from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    is_superuser:bool = False
    
class SuperUserCreate(UserCreate):
    is_superuser:bool = True

class UserOut(BaseModel):
    id: int
    username: str
    is_superuser:bool

    class Config:
        orm_mode = True
