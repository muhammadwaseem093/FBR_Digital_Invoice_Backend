from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    superadmin = "superadmin"
    tenant_admin = "tenant_admin"
    employee = "employee"

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_superuser: Optional[bool] = False   # ✅ ADD THIS
    role: Optional[UserRole] = None        # ✅ ADD THIS
    tenant_id: Optional[UUID4] = None      # ✅ ADD THIS

class UserOut(UserBase):
    id: UUID4
    is_superuser: bool
    role: UserRole
    tenant_id: Optional[UUID4]
    is_active: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
