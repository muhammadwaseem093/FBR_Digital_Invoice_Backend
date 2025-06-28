from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserOut, SuperUserCreate
from app.db.models import User 
from app.core.security import hash_password 
from app.db.database import SessionLocal
from app.core.security import get_current_user 

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
@router.post("/", response_model=UserOut)
def create_user(
    data:UserCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
    ):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=data.username, password=hash_password(data.password), is_superuser=data.is_superuser)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/create-superuser", response_model=UserOut)
def create_superuser(data:SuperUserCreate, db:Session = Depends(get_db)):
    existing =db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username Already Exists")
    
    new_user = User(
        username=data.username,
        password=hash_password(data.password),
        is_superuser=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user