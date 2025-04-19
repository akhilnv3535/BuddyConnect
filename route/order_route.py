from fastapi import APIRouter

from core.db import SessionDep
from route.models import OrderCreate, Order

route = APIRouter(prefix="/orders", tags=["Order"])


@route.post("/")
def create_order(order: OrderCreate, session: SessionDep) -> Order:
    orde = Order(**order.model_dump())
    orde.service_hours = (orde.end_time - orde.start_time).total_seconds() / 3600
    print("Order time: ", orde.service_hours)
    session.add(orde)
    session.commit()
    session.refresh(orde)
    return orde


@route.post("/{order_id}")
def fetch_order(order_id: int, session: SessionDep) -> Order:
    order = session.query(Order).filter(Order.id == order_id).first()
    return order
