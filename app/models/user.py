import uuid
import enum
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base  # Adjust path if your Base is elsewhere

# Define User roles
class UserRole(str, enum.Enum):
    superadmin = "superadmin"        # System-level superuser (only one)
    tenant_admin = "tenant_admin"    # Tenant-level admin, manages their own users
    employee = "employee"            # Normal user under a tenant

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.employee)

    # Relationship to support tenant -> employees
    employees = relationship("User", remote_side=[id], backref="tenant", cascade="all, delete")
