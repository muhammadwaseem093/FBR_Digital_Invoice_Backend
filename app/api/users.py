from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserOut
from app.services import user_services
from app.core.security import get_current_user
from app.dependencies.auth_guards import tenant_admin_only, superuser_only
from app.models.user import User

router = APIRouter()

@router.post("", response_model=UserOut)
def create_employee(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(tenant_admin_only)
):
    if user_services.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.is_superuser = False
    user.role = "employee"
    user.tenant_id = current_user.id
    return user_services.create_user(db, user)

@router.get("", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(superuser_only)):
    return user_services.get_users(db)

@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
