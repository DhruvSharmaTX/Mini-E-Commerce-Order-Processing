from pydantic import BaseModel
from datetime import datetime
from typing import List


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: str
    user_id: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True