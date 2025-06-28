from passlib.context import CryptContext
from cryptography.fernet import Fernet 
from fastapi import Depends, HTTPException 
from fastapi.security import OAuth2PasswordBearer
from app.db.models import User
from jose import jwt, JWTError
import os 
from app.db.database import SessionLocal
from datetime import datetime, timedelta 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM="HS256"
SECRET_ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(SECRET_ENCRYPTION_KEY.encode())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password):
    return pwd_context.hash(password)
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data, expires_delta=60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        db = SessionLocal()
        user = db.query(User).filter(User.username ==username).first()
        db.close()
        
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
def encrypt_data