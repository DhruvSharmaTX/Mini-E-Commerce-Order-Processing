from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(15), primary_key=True, index=True)
    order_id = Column(String(15), ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(String(15), ForeignKey("products.id"), nullable=False, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")