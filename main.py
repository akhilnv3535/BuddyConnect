from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.db import engine
from route.category_route import cat_route
# from route.hero_route import route as hero_route
from route.models import SQLModel
from route.user_route import route as user_route

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


@app.get('ping')
def ping():
    return "pong"
