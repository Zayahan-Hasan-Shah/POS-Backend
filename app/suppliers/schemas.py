from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    company_name: str


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    company_name: str
    created_at: datetime

    class Config:
        orm_mode = True
