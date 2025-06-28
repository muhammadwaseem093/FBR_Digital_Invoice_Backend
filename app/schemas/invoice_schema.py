from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    invoice_no:str
    amount:float
    
    
class InvoiceOut(BaseModel):
    id:int 
    invoice_no:str
    amount:float
    qr_code_path:str
    pdf_path:str
    
    class Config:
        orm_mode = True