from typing import Optional

from pydantic import BaseModel


class HeroSchema(BaseModel):
    # id: int
    name: str
    age: Optional[int] = None
