from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.user import User

def superuser_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Superadmin access only")
    return current_user

def tenant_admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "tenant_admin":
        raise HTTPException(status_code=403, detail="Tenant admin access only")
    return current_user