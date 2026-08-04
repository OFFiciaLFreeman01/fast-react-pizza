from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pizza import Pizza
from app.schemas.pizza import PizzaOut

router = APIRouter(prefix="/api/v1/menu", tags=["menu"])


def serialize_pizza(pizza: Pizza) -> PizzaOut:
    return PizzaOut(
        id=pizza.id,
        name=pizza.name,
        ingredients=pizza.ingredients.split(","),
        unit_price=float(pizza.unit_price),
        image_url=pizza.image_url,
        sold_out=pizza.sold_out,
    )


@router.get("", response_model=list[PizzaOut])
def get_menu(db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).order_by(Pizza.id).all()
    return [serialize_pizza(p) for p in pizzas]
