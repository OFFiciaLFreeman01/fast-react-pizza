from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import require_admin
from app.models.order import Order, OrderItem, generate_order_id
from app.models.pizza import Pizza
from app.schemas.order import OrderCreate, OrderPriorityUpdate, OrderStatusUpdate

router = APIRouter(prefix="/api/v1/order", tags=["orders"])

PRIORITY_FEE_RATE = Decimal("0.2")
BASE_DELIVERY_MINUTES = 30
PRIORITY_TIME_SAVED_MINUTES = 10

# Kitchen staff can only move an order forward one step at a time.
VALID_STATUS_TRANSITIONS = {
    "preparing": {"out-for-delivery"},
    "out-for-delivery": {"delivered"},
    "delivered": set(),
}


def serialize_order(order: Order) -> dict:
    subtotal = sum(Decimal(str(i.unit_price)) * i.quantity for i in order.items)
    priority_price = subtotal * PRIORITY_FEE_RATE if order.priority else Decimal("0")
    return {
        "id": order.id,
        "customer": order.customer,
        "phone": order.phone,
        "address": order.address,
        "priority": order.priority,
        "status": order.status,
        "orderPrice": float(subtotal),
        "priorityPrice": float(priority_price),
        "items": [
            {
                "pizza_id": i.pizza_id,
                "name": i.name,
                "quantity": i.quantity,
                "unit_price": float(i.unit_price),
            }
            for i in order.items
        ],
        "estimated_delivery": order.estimated_delivery.isoformat(),
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }


@router.post("")
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    pizza_ids = [item.pizza_id for item in body.cart]
    pizzas = {p.id: p for p in db.query(Pizza).filter(Pizza.id.in_(pizza_ids)).all()}

    missing = [pid for pid in pizza_ids if pid not in pizzas]
    if missing:
        raise HTTPException(status_code=400, detail=f"Unknown pizza id(s): {missing}")

    sold_out = [pizzas[pid].name for pid in pizza_ids if pizzas[pid].sold_out]
    if sold_out:
        raise HTTPException(status_code=400, detail=f"Sold out: {', '.join(sold_out)}")

    time_saved = PRIORITY_TIME_SAVED_MINUTES if body.priority else 0
    estimated_delivery = datetime.now(timezone.utc) + timedelta(
        minutes=BASE_DELIVERY_MINUTES - time_saved
    )

    order = Order(
        id=generate_order_id(),
        customer=body.customer,
        phone=body.phone,
        address=body.address,
        priority=body.priority,
        status="preparing",
        estimated_delivery=estimated_delivery,
    )
    db.add(order)
    db.flush()

    for item in body.cart:
        pizza = pizzas[item.pizza_id]
        db.add(
            OrderItem(
                order_id=order.id,
                pizza_id=pizza.id,
                name=pizza.name,
                quantity=item.quantity,
                unit_price=pizza.unit_price,
            )
        )

    db.commit()
    db.refresh(order)
    return serialize_order(order)


@router.get("")
def list_orders(
    status: str | None = None,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
):
    query = db.query(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc())
    if status:
        query = query.filter(Order.status == status)
    return [serialize_order(o) for o in query.all()]


@router.get("/{order_id}")
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found")
    return serialize_order(order)


@router.patch("/{order_id}")
def update_order_priority(order_id: str, body: OrderPriorityUpdate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found")
    order.priority = body.priority
    db.commit()
    db.refresh(order)
    return serialize_order(order)


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: str,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found")

    if body.status != order.status and body.status not in VALID_STATUS_TRANSITIONS[order.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot move order from '{order.status}' to '{body.status}'",
        )

    order.status = body.status
    db.commit()
    db.refresh(order)
    return serialize_order(order)
