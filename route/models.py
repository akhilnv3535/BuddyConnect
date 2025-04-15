from datetime import datetime
from typing import Optional, List

from pydantic import EmailStr
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


#  Booking confirmation
# Services
# Category
# SubCategory

class SavedAddress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    save_as: str
    house_flat_no: Optional[str] = Field(default=None, nullable=True)
    address: str
    description: Optional[str] = Field(default=None, nullable=True)
    pincode: Optional[int] = Field(default=None, nullable=True)
    user_id: Optional[int] = Field(default=None, foreign_key="customerusers.id")
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


class CustomerUsers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=False)
    profile_pic: str | None = None
    mobile_no: str = Field(max_length=15, unique=True, nullable=False)
    email: EmailStr | None = Field(default=None, unique=True)
    # saved_address: List[SavedAddress] = Relationship(back_populates="customerusers")
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


class CustomerUsersCreate(SQLModel):
    name: str = Field(index=True, unique=False)
    profile_pic: str | None = None
    mobile_no: int
    email: EmailStr | None = Field(default=None)


class SavedAddressCreate(SQLModel):
    save_as: str
    house_flat_no: Optional[str] = None
    address: str
    description: Optional[str] = None
    user_id: int
    pincode: int


class PartnerUsers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    profile_pic: str | None = None
    mobile_no: str = Field(max_length=15, unique=True)
    email: EmailStr | None = Field(default=None, unique=True)

    panId: Optional[str] = Field(default=None, max_length=10, unique=True)
    aadharID: Optional[str] = Field(default=None, max_length=12, unique=True)
    bankAccount: Optional[str] = Field(default=None, max_length=30)
    ifscCode: Optional[str] = Field(default=None, max_length=11)
    address: Optional[str] = Field(default=None, nullable=False)
    preferredLocation: Optional[str] = Field(default=None)
    bloodGroup: Optional[str] = Field(default=None)
    primarySkills: Optional[str] = Field(default=None)
    secondarySkills: Optional[str] = Field(default=None)
    created: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )
    modified: Optional[datetime] = Field(
        default_factory=lambda: now_utc()
    )


class PartnerUsersCreate(SQLModel):
    name: str
    profile_pic: Optional[str] = None
    mobile_no: Optional[str] = None
    email: EmailStr | None = Field(default=None)
    panId: Optional[str] = None
    aadharID: Optional[str] = None
    bankAccount: Optional[str] = None
    ifscCode: Optional[str] = None
    address: Optional[str] = None
    preferredLocation: Optional[str] = None
    bloodGroup: Optional[str] = None
    primarySkills: Optional[str] = None
    secondarySkills: Optional[str] = None


class PartnerUsersResponse(SQLModel):
    id: int
    name: str
    profile_pic: Optional[str] = None
    mobile_no: str
    email: EmailStr
