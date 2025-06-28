from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
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
    new_cred = Credential(api_key=data.api_key, api_secret=data.api_secret, user_id=current_user.id)
    db.add(new_cred)
    db.commit()
    db.refresh(new_cred)

    return {
        "id": new_cred.id,
        "api_key": new_cred.api_key,
        "api_secret": new_cred.api_secret
    }

@router.get("/", response_model=list[CredentialOut])
def get_own_credentials(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    creds = db.query(Credential).filter(Credential.user_id == current_user.id).all()
    return [
        {
            "id": c.id,
            "api_key": c.api_key,
            "api_secret": c.api_secret
        } for c in creds
    ]
