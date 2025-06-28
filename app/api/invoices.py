from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from app.schemas.invoice_schema import InvoiceCreate, InvoiceOut
from app.db.models import Invoice
from app.db.database import SessionLocal 
import os, qrcode 
from reportlab.pdfgen import canvas

router = APIRouter()

OUTPUT_DIR = "generated_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
        
@router.post("/{user_id}", response_model = InvoiceOut)
def create_invoice(user_id:int, data:InvoiceCreate, db:Session=Depends(get_db)):
    qr_path = f"{OUTPUT_DIR}/qr_{data.invoice_no}.png"
    pdf_path = f"{OUTPUT_DIR}/invoice_{data.invoice_no}.pdf"
    
    qr = qrcode.make(f"FBR Invoice: {data.invoice_no}")
    qr.save(qr_path)
    
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, f"Invoice No: {data.invoice_no}")
    c.drawString(100, 730, f"Amount Rs. {data.amount}")
    c.drawImage(qr_path, 100,650, width=100, height=100)
    c.save()
    
    invoice = Invoice(invoice_no=data.invoice_no, amount=data.amount, qr_code=qr_path, pdf_path=pdf_path, user_id=user_id, posted=True)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice