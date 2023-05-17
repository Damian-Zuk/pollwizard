from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    
class UserLogin(UserBase):
    password: str

class UserCreate(UserLogin):
    name: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True