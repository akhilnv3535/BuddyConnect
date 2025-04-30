from fastapi import APIRouter, HTTPException, WebSocket

from core.db import SessionDep
from route.connection_manager import ConnectionManager
from route.models import OrderCreate, Order, OrderUpdate, CustomerUsers, PartnerUsers
from utils import now_utc

route = APIRouter(prefix="/orders", tags=["Order"])

manager = ConnectionManager()


@route.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive; you can add handling for incoming messages if needed
            data = await websocket.receive_text()
            print("data received: ", data)
    except Exception as e:
        manager.disconnect(websocket)


# WebSocket endpoint for employees
# @route.websocket("/ws/orders1")
# async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
#     await manager.connect(websocket)
#     try:
#         while True:
#             # Receive messages from the employee (e.g., to accept an order)
#             data = await websocket.receive_json()
#             print("socket res: ", data)
#             action = data.get("action")
#             order_id = data.get("order_id")
#             print("order_id: ", order_id)
#             partner_id = data.get("partner_id")  # Unique identifier for the employee
#
#             if action == "accept_order":
#                 print('Order accepted')
#                 # Find the order in the database
#                 order = session.query(Order).filter(Order.id == order_id).first()
#                 print("Order: ", order)
#                 if order:
#                     print("Order available")
#
#                 if not order:
#                     print("not Order")
#                     await websocket.send_json({"error": "Order not found"})
#                     continue
#
#                 # Check if the order is already accepted
#                 if order["status"] == "accepted":
#                     print("Status accepted")
#                     await websocket.send_json({"error": "Order already accepted"})
#                     continue
#
#                 # Update the order status and accepted_by field
#
#                 update_order_accepted(order_id, partner_id, session)
#
#                 # Broadcast the updated order to all clients
#                 await manager.broadcast({
#                     "id": order["id"],
#                     "status": "accepted",
#                     "accepted_by": partner_id,
#                     "message": f"Order {order_id} accepted by {partner_id}"
#                 })
#
#     except Exception as e:
#         manager.disconnect(websocket)
#

@route.post("/")
async def create_order(order: OrderCreate, session: SessionDep) -> Order:
    orde = Order(**order.model_dump())
    orde.service_hours = (orde.end_time - orde.start_time).total_seconds() / 3600
    session.add(orde)
    session.commit()
    session.refresh(orde)
    json_data = {
        "event": "new_order",
        "data": {
            "id": orde.id,
            "service_hours": orde.service_hours,
            "earnings": orde.earnings,
            "address": orde.address
        }
    }
    await manager.broadcast(json_data)
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


@route.post("/accept/{order_id}")
def update_order_accepted(order_id: int, partner_id: int, session: SessionDep):
    try:
        print("order id: ", order_id)
        print("order partner id: ", partner_id)
        orde = session.query(Order).filter(Order.id == order_id).first()
        if orde.is_accepted:
            raise HTTPException(status_code=400, detail="Order already accepted")
        orde.is_accepted = True
        orde.partner_id = partner_id
        orde.accepted_at = now_utc()
        orde.modified = now_utc()
        session.commit()
        session.refresh(orde)
        return True
    except Exception as e:
        print('error update: ', e)
        return False


@route.get("/all-details")
def get_all_details(session: SessionDep):
    users_count = session.query(CustomerUsers).count()
    partners_count = session.query(PartnerUsers).count()
    pending_partners = session.query(PartnerUsers).where(PartnerUsers.approval_status == "pending").count()
    rejected_partners = session.query(PartnerUsers).where(PartnerUsers.approval_status == "rejected").count()
    approved_partners = session.query(PartnerUsers).where(PartnerUsers.approval_status == "rejected").count()
    orders_count = session.query(PartnerUsers).count()
    return {"users_count": users_count, "orders_count": orders_count, "partners_count": partners_count,
            "approved_partners": approved_partners, "rejected_partners": rejected_partners,
            "pending_partners": pending_partners}
