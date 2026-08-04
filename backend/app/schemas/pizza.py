from pydantic import BaseModel


class PizzaOut(BaseModel):
    id: int
    name: str
    ingredients: list[str]
    unit_price: float
    image_url: str
    sold_out: bool
