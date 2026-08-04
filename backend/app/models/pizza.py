from sqlalchemy import Boolean, Column, Integer, Numeric, String

from app.database import Base


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)  # comma-separated
    unit_price = Column(Numeric(6, 2), nullable=False)
    image_url = Column(String, nullable=False)
    sold_out = Column(Boolean, nullable=False, default=False)
