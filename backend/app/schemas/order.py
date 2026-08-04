from typing import Literal

from pydantic import BaseModel, field_validator


class CartItemIn(BaseModel):
    pizza_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        return v


class OrderCreate(BaseModel):
    customer: str
    phone: str
    address: str
    priority: bool = False
    cart: list[CartItemIn]

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) < 7:
            raise ValueError("Phone number looks invalid")
        return v

    @field_validator("cart")
    @classmethod
    def cart_not_empty(cls, v: list[CartItemIn]) -> list[CartItemIn]:
        if not v:
            raise ValueError("Cart cannot be empty")
        return v


class OrderPriorityUpdate(BaseModel):
    priority: bool


class OrderStatusUpdate(BaseModel):
    status: Literal["preparing", "out-for-delivery", "delivered"]
