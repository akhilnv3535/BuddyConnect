from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.db import engine
from route.hero_route import route as hero_route
from route.models import SQLModel

# SessionDep = Annotated[Session, Depends(get_db)]
SQLModel.metadata.create_all(engine)

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(hero_route)