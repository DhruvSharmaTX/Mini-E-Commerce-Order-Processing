from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from collections import defaultdict

from backend.app.models.order_model import Order
from backend.app.models.product_model import Product
from backend.app.models.user_model import User
from backend.app.models.order_item_model import OrderItem
from backend.app.schemas.order_schema import OrderCreate
from backend.app.utils.id_service import unique_id

def create_order(db: Session, order_data: OrderCreate):
    try:
        user = db.query(User).filter(User.id == order_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=" ot found")

        total_amount = 0
        products_cache = {}
        quantity_tracker = defaultdict(int)

        for item in order_data.items:
            quantity_tracker[item.product_id] += item.quantity

        for product_id, total_qty in quantity_tracker.items():

            product = (
                db.query(Product)
                .filter(Product.id == product_id)
                .with_for_update() 
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {product_id} not found"
                )

            if product.quantity < total_qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Only {product.quantity} available for {product.name}"
                )

            total_amount += product.price * total_qty
            products_cache[product_id] = product

        order_id = unique_id(db, Order, "O")

        new_order = Order(
            id=order_id,
            user_id=order_data.user_id,
            total_amount=total_amount,
            status="created"
        )

        db.add(new_order)
        db.flush()

        last_item = (
            db.query(OrderItem)
            .order_by(desc(OrderItem.id))
            .with_for_update()
            .first()
        )

        if last_item:
            current_number = int(last_item.id.replace("OI", ""))
        else:
            current_number = 0

        for product_id, total_qty in quantity_tracker.items():
            product = products_cache[product_id]

            product.quantity -= total_qty

            current_number += 1
            new_item_id = f"OI{current_number:03d}"

            order_item = OrderItem(
                id=new_item_id,
                order_id=order_id,
                product_id=product_id,
                price=product.price,
                quantity=total_qty
            )

            db.add(order_item)

        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception as e:
        db.rollback()
        raise e


def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="not found")

    return order


def cancel_order(db: Session, order_id: str):

    try:
        order = (
            db.query(Order)
            .filter(Order.id == order_id)
            .with_for_update()
            .first()
        )

        if not order:
            raise HTTPException(status_code=404, detail="not found")

        if order.status == "cancelled":
            raise HTTPException(status_code=400, detail="already cancelled")

        for item in order.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if product:
                product.quantity += item.quantity

        order.status = "cancelled"

        db.commit()
        db.refresh(order)

        return order

    except Exception as e:
        db.rollback()
        raise e