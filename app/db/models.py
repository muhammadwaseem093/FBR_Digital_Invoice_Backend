from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship 
from .database import Base 
from datetime import datetime



class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,  unique=True, index=True)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    
    credentials = relationship("Credential", back_populates="owner")
    invoices = relationship("Invoice", back_populates="owner")
    

class Credential(Base):
    __tablename__="credentials"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    api_secret = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    
    owner = relationship("User", back_populates="credentials")
    
    
class Invoice(Base):
    __tablename__="invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String, unique=True)
    qr_code_path = Column(String)
    pdf_path = Column(String)
    amount=Column(Float)
    posted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="invoices")
    