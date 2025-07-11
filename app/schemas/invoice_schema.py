from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    hsCode: str
    productDescription: str
    rate: str
    uoM: str
    quantity: float
    totalValues: float
    valueSalesExcludingST: str
    salesTaxApplicable: str
    fixedNotifiedValueOrRetailPrice: float
    salesTaxWithheldAtSource: float
    extraTax: str
    furtherTax: float
    sroScheduleNo: str
    fedPayable: float
    discount: float
    saleType: str
    sroItemSerialNo: str

class InvoiceCreate(BaseModel):
    invoiceType: str
    sellerBusinessName: str
    sellerProvince: str
    sellerAddress: str
    buyerNTNCNIC: str
    buyerBusinessName: str
    buyerProvince: str
    buyerAddress: str
    buyerRegistrationType: str
    scenarioId: str
    items: List[InvoiceItem]
