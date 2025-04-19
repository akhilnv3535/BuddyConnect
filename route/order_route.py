from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from route.models import OrderCreate, Order, OrderUpdate
from utils import now_utc

route = APIRouter(prefix="/orders", tags=["Order"])


@route.post("/")
def create_order(order: OrderCreate, session: SessionDep) -> Order:
    orde = Order(**order.model_dump())
    orde.service_hours = (orde.end_time - orde.start_time).total_seconds() / 3600
    session.add(orde)
    session.commit()
    session.refresh(orde)
    return orde


@route.post("/{order_id}")
def fetch_order_details(order_id: int, session: SessionDep) -> Order:
    order = session.query(Order).filter(Order.id == order_id).first()
    return order


@route.get("/user/{user_id}")
def fetch_user_orders(user_id: int, session: SessionDep) -> list[Order]:
    order = session.query(Order).filter(Order.user_id == user_id)
    return order


@route.patch("/{order_id}")
def update_orders(order_id: int, data: OrderUpdate, session: SessionDep):
    record = session.get(Order, order_id)
    if not record:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(record, key, value)

    record.modified = now_utc()
    session.commit()
    session.refresh(record)
    return {"ok": "success"}


@route.post("/cancel/{order_id}")
def cancel_order(order_id: int, session: SessionDep):
    record = session.get(Order, order_id)
    if not record:
        raise HTTPException(status_code=404, detail="Order not found")
    record.is_cancelled = True
    record.modified = now_utc()
    session.add(record)
    session.commit()
    session.refresh(record)
    return {"ok": "success"}
