from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.app.models.product_model import Product
from backend.app.schemas.product_schema import ProductCreate
from backend.app.utils.id_service import unique_id


def create_product(db: Session, product_data: ProductCreate):
    try:
        existing_name = db.query(Product).filter(
            Product.name == product_data.name
        ).first()

        if existing_name:
            raise HTTPException(status_code=400, detail="already exists")

        product_id = unique_id(db, Product, "P")

        new_product = Product(
            id=product_id,
            name=product_data.name,
            price=product_data.price,
            quantity=product_data.quantity  
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product

    except Exception:
        db.rollback()
        raise