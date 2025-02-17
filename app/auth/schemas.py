from typing import Optional
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    username: str
    email: str
    phone_number: str
    password: str
    shopname: str
    shop_address: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    shop_address: Optional[str] = None
    shopname: Optional[str] = None
    
    class Config:
        orm_mode = True