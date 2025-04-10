from datetime import timezone, datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


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


class SubCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="subcategories")
    created: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    subcategories: List[SubCategory] = Relationship(back_populates="category")
    created: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CategoryCreate(SQLModel):
    name: str


class SubCategoryCreate(SQLModel):
    name: str
    category_id: int
