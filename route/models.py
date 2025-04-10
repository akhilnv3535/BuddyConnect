from datetime import timezone, datetime
from typing import Optional

from sqlmodel import SQLModel, Field


def now_utc():
    return datetime.now(timezone.utc)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: Optional[str] = None
    created: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
