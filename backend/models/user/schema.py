from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    password: str
    name: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
