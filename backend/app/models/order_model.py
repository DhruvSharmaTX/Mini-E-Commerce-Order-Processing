from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from backend.app.database.connection import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(15), primary_key=True, index=True)
    user_id = Column(String(15), ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")