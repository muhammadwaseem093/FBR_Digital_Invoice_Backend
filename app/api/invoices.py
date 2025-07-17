from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import httpx
import logging

app = FastAPI()

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class InvoiceItem(BaseModel):
    hsCode: str
    productDescription: str
    rate: str
    uoM: str
    quantity: int
    totalValues: float
    valueSalesExcludingST: float
    salesTaxApplicable: float
    saleType: str

class InvoiceRequest(BaseModel):
    buyerNTNCNIC: str
    buyerBusinessName: str
    items: List[InvoiceItem]
    invoiceType: Optional[str] = "Sale Invoice"
    invoiceDate: Optional[str] = None

class FBRResponse(BaseModel):
    success: bool
    message: str
    fbr_receipt: Optional[dict] = None
    errors: Optional[List[str]] = None

# Configuration
FBR_CONFIG = {
    "BASE_URL": "https://gw.fbr.gov.pk/di_data/v1/di",
    "TOKEN": "d48a0893-72a5-3d89-ac69-6abf9acc61b0",
    "TIMEOUT": 30
}


def generate_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FBR_CONFIG['TOKEN']}",
        "REQUEST-TIMESTAMP": datetime.now().strftime("%Y%m%d%H%M%S"),
        "DEVICE-TYPE": "API",
        "ACCEPT-LANGUAGE": "en-US"
    }

def validate_invoice(data: dict):
    """Validate and complete invoice data"""
    # Required field checks
    if len(data["buyerNTNCNIC"]) not in [13, 15]:
        raise ValueError("NTN/CNIC must be 13 or 15 digits")
    
    # Date handling
    if not data.get("invoiceDate"):
        data["invoiceDate"] = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(data["invoiceDate"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    # Add mandatory seller info (replace with your actual details)
    data.update({
        "sellerBusinessName": "Your Registered Business",
        "sellerNTN": "1234567890123",
        "sellerAddress": "123 Business Street, Karachi",
        "invoiceRefNo": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "buyerRegistrationType": "Registered",
        "scenarioId": "SN001"
    })
    
    # Validate items
    for item in data["items"]:
        if item["quantity"] <= 0:
            raise ValueError("Quantity must be greater than 0")
    
    return data

@router.post("/invoices/submit", response_model=FBRResponse)
async def submit_invoice(invoice: InvoiceRequest):
    """Submit invoice to FBR Sandbox"""
    try:
        # Prepare and validate invoice
        invoice_data = validate_invoice(invoice.dict())
        headers = generate_headers()
        url = f"{FBR_CONFIG['BASE_URL']}/postinvoicedata_sb"

        logger.info(f"Submitting invoice to FBR: {invoice_data}")

        # Make API call
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=invoice_data,
                headers=headers,
                timeout=FBR_CONFIG["TIMEOUT"]
            )

        # Handle response
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Invoice submitted successfully",
                "fbr_receipt": response.json()
            }
        else:
            error_msg = f"FBR API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": "FBR rejected the invoice",
                "errors": [error_msg]
            }

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return {
            "success": False,
            "message": "Invalid invoice data",
            "errors": [str(ve)]
        }
    except httpx.RequestError as re:
        logger.error(f"Network error: {str(re)}")
        return {
            "success": False,
            "message": "Failed to connect to FBR",
            "errors": [str(re)]
        }
    except Exception as e:
        logger.exception("Unexpected error")
        return {
            "success": False,
            "message": "Internal server error",
            "errors": [str(e)]
        }

# Sample Test Endpoint
@router.get("/invoices/test")
async def test_endpoint():
    """Test endpoint with sample data"""
    sample_data = {
        "buyerNTNCNIC": "1234567890123",
        "buyerBusinessName": "Test Buyer",
        "items": [{
            "hsCode": "8542.3100",
            "productDescription": "Test Product",
            "rate": "17%",
            "uoM": "PCS",
            "quantity": 1,
            "totalValues": 1000,
            "valueSalesExcludingST": 854.70,
            "salesTaxApplicable": 145.30,
            "saleType": "Local"
        }],
        "invoiceType": "Sale Invoice",
        "invoiceDate": datetime.now().strftime("%Y-%m-%d")
    }
    return sample_data