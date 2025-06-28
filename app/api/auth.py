from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal 
from app.db import models 
from app.core.security import verify_password, create_token 
from pydantic import BaseModel 

router = APIRouter()

class LoginSchema(BaseModel):
    username:str 
    password:str 
    
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
        
@router.post("/login")
def login(data:LoginSchema, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = create_token({"sub": user.username})
    return {"access_token": token, "is_superuser": user.is_superuser}