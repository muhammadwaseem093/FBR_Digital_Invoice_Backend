from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserOut
from app.services import user_services
from app.models.user import User
from uuid import uuid4
from app.dependencies.auth_guards import superuser_only

router = APIRouter()

@router.post("/superuser", response_model=UserOut)
def create_superadmin(user: UserCreate, db: Session = Depends(get_db)):
    existing_super = db.query(User).filter(User.role == "superadmin").first()
    if existing_super:
        raise HTTPException(403, detail="Superadmin already exists")

    return user_services.create_user(
        db,
        user,
        is_superuser=True,
        role="superadmin",
        tenant_id=None
    )

@router.post("/tenantuser", response_model=UserOut)
def create_tenant_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(superuser_only)  # Only superadmin can create tenants
):
    tenant_id = uuid4()  # ✅ assign a fresh tenant ID to tenant admin
    return user_services.create_user(
        db,
        user,
        is_superuser=True,
        role="tenant_admin",
        tenant_id=tenant_id
    )
