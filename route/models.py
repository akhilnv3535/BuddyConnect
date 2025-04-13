from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from utils import now_utc


class Services(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    icon: str | None = None
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: Optional[str] = None
#     created: Optional[datetime] = Field(
#         default_factory=lambda: datetime.now(timezone.utc)
#     )
#     modified: Optional[datetime] = Field(
#         default_factory=lambda: datetime.now(timezone.utc)
#     )


class SubCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    icon: str | None = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="subcategories")
    service_id: Optional[int] = Field(default=None, foreign_key="services.id")
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    icon: str | None = None
    service_id: Optional[int] = Field(default=None, foreign_key="services.id")
    subcategories: List[SubCategory] = Relationship(back_populates="category")
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


class ServicesCreate(SQLModel):
    name: str
    icon: Optional[str] = None


class CategoryCreate(SQLModel):
    name: str
    service_id: int
    icon: Optional[str] = None


class SubCategoryCreate(SQLModel):
    name: str
    category_id: int
    service_id: int
    icon: Optional[str] = None
