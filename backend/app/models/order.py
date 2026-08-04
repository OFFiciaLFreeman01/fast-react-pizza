import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base


def generate_order_id() -> str:
    return uuid.uuid4().hex[:8].upper()


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=generate_order_id)
    customer = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    priority = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="preparing")
    estimated_delivery = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(6, 2), nullable=False)

    order = relationship("Order", back_populates="items")
