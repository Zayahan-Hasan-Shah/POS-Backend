from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceItemRequest(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

class InvoiceRequest(BaseModel):
    customer_name: Optional[str] = Field(default="Anonymous")
    customer_phone: Optional[str] = Field(default="1234567890")
    items: List[InvoiceItemRequest]
