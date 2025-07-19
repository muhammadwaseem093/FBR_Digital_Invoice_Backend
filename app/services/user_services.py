from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from uuid import UUID

def create_user(
    db: Session,
    user: UserCreate,
    is_superuser: bool,
    role: str,
    tenant_id: UUID = None
):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_superuser=is_superuser,
        role=role,
        tenant_id=tenant_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
