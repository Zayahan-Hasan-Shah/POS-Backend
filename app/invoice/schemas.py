# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime
# from pydantic import Field
# class InvoiceItemRequest(BaseModel):
#     product_name: str
#     quantity: int
#     unit_price: float

# class InvoiceRequest(BaseModel):
#     customer_name: Optional[str] = Field(default="Anonymous")
#     customer_phone: Optional[str] = Field(default="1234567890")
#     items: List[InvoiceItemRequest]

# #########################################

# class InvoiceItemCreate(BaseModel):
#     product_name: str
#     quantity: int
#     unit_price: float
#     total_price: float

# class InvoiceCreate(BaseModel):
#     customer_id: int
#     items: List[InvoiceItemCreate]
#     total_amount: float
#     payment_method: str

# class InvoiceItemResponse(BaseModel):
#     id: int
#     product_name: str
#     quantity: int
#     unit_price: float
#     total_price: float

#     class Config:
#         orm_mode = True

# class InvoiceResponse(BaseModel):
#     id: int
#     invoice_number: str
#     customer_id: int
#     total_amount: float
#     payment_method: str
#     status: str
#     created_at: datetime
#     items: List[InvoiceItemResponse]

#     class Config:
#         orm_mode = True



# from sqlalchemy.orm import Session
# from typing import List
# from datetime import datetime
# from app.database import get_db
# from app.invoice.models import Invoice, InvoiceItem
# from pydantic import BaseModel


# class InvoiceItemCreate(BaseModel):
#     product_name: str
#     quantity: int
#     unit_price: float
#     total_price: float

# class InvoiceCreate(BaseModel):
#     customer_name: str
#     customer_phone: str
#     total_amount: float
#     payment_method: str
#     items: List[InvoiceItemCreate]

from pydantic import BaseModel
from typing import List
from datetime import datetime

class InvoiceItemBase(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int

    class Config:
        from_attributes = True  # For Pydantic v2, use this instead of orm_mode

class InvoiceBase(BaseModel):
    customer_name: str
    customer_phone: str
    total_amount: float

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]

class Invoice(InvoiceBase):
    id: int
    invoice_number: str  # Changed from customer_phone_invoice_number
    created_at: datetime
    items: List[InvoiceItem]

    class Config:
        from_attributes = True

