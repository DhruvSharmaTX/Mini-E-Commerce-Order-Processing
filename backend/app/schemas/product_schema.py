from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True