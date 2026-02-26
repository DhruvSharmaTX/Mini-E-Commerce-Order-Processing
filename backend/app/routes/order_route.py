from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database.connection import get_db
from backend.app.models.order_model import Order
from backend.app.schemas.order_schema import OrderCreate, OrderResponse
from backend.app.services.order_service import (
    create_order as create_order_service,
    cancel_order as cancel_order_service
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(db, order)


@router.put("/cancel/{order_id}", response_model=OrderResponse)
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    return cancel_order_service(db, order_id)