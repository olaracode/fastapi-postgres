from pydantic import BaseModel

# Pydantic Schemas for src.models:User

class BaseUser(BaseModel):
    email: str
    
class UserCreate(BaseUser):
    password: str

class UserInDB(BaseUser):
    id: int
    hashed_password: str
    class Config:
        orm_mode = True