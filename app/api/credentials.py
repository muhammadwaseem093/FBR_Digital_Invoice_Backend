from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user, encrypt_data, decrypt_data
from app.schemas.credential_schema import CredentialCreate, CredentialOut
from app.db.database import SessionLocal
from app.db.models import Credential

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CredentialOut)
def create_credential(data: CredentialCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    encrypted_key = encrypt_data(data.api_key)
    encrypted_secret = encrypt_data(data.api_secret)

    new_cred = Credential(api_key=encrypted_key, api_secret=encrypted_secret, user_id=current_user.id)
    db.add(new_cred)
    db.commit()
    db.refresh(new_cred)

    return {
        "id": new_cred.id,
        "api_key": data.api_key,  # Show decrypted for response
        "api_secret": data.api_secret
    }

@router.get("/", response_model=list[CredentialOut])
def get_own_credentials(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    creds = db.query(Credential).filter(Credential.user_id == current_user.id).all()
    return [
        {
            "id": c.id,
            "api_key": decrypt_data(c.api_key),
            "api_secret": decrypt_data(c.api_secret)
        } for c in creds
    ]
