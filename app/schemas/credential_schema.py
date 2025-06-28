from pydantic import BaseModel

class CredentialCreate(BaseModel):
    api_key : str
    api_secret:str
    
class CredentialOut(BaseModel):
    id:int
    api_key:str
    api_secret:str
    
    class Config:
        orm_mode=True
        
        