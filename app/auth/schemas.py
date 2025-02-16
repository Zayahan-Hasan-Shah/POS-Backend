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
