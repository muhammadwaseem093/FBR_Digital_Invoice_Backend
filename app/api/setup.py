from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserOut
from app.services import user_services
from app.core.security import get_current_user
from app.dependencies.auth_guards import superuser_only
import uuid
from app.models.user import User

router = APIRouter()

@router.post("/superuser", response_model=UserOut)
def create_superadmin(user: UserCreate, db: Session = Depends(get_db)):
    existing_super = db.query(User).filter(User.role == "superadmin").first()
    if existing_super:
        raise HTTPException(403, detail="Superadmin already exists")

    user.is_superuser = True
    user.role = "superadmin"
    user.tenant_id = None
    return user_services.create_user(db, user)

@router.post("/tenantuser", response_model=UserOut)
def create_tenant_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(superuser_only)
):
    user.is_superuser = True
    user.role = "tenant_admin"
    user.tenant_id = None
    return user_services.create_user(db, user)