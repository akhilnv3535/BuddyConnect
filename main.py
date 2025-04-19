from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

from core.db import engine, async_session
from route.category_route import cat_route
from route.connection_manager import ConnectionManager
# from route.hero_route import route as hero_route
from route.models import SQLModel, Order
from route.order_route import route as order_route
from route.user_route import route as user_route
from utils import now_utc

SQLModel.metadata.create_all(engine)

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(cat_route)
app.include_router(user_route)
app.include_router(order_route)


@app.get('ping')
def ping():
    return "pong"


manager = ConnectionManager()


@app.websocket("/ws/order-notify")
async def webscoket_order(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        data = await websocket.receive_json()

        if data.get('type') == "accept_offer":
            order_id = data.get("order_id")

            async with async_session() as db:
                offer = await db.query(Order).filter(Order.id == order_id).first()
                if not offer:
                    await websocket.send_json({
                        "type": "error",
                        "message": "offer not found"
                    })
                    # continue
                if offer.is_accepted:
                    await websocket.send_json({
                        "type": "error",
                        "message": "offer already accepted"
                    })
                    # continue

                offer.is_accepted = True
                offer.accepted_at = lambda: now_utc()
                await db.commit()

                await manager.broadcast({
                    "type": "offer_accepted",
                    "offer_id": offer.id,
                    "accepted_at": str(offer.accepted_at)
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
