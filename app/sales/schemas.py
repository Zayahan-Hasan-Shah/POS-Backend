from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SaleRequest(BaseModel):
    product_id: int
    quantity: int
    payment_method: str

class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    payment_method: str
    created_at: datetime
