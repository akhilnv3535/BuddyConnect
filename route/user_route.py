from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from core.db import SessionDep
from route.models import CustomerUsers, CustomerUsersCreate, SavedAddress, SavedAddressCreate, PartnerUsersCreate, \
    PartnerUsers

route = APIRouter(prefix="/user", tags=["Users"])


@route.get("/")
def read_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=20)] = 20,
) -> list[CustomerUsers]:
    users = session.query(CustomerUsers).offset(offset).limit(limit).all()
    return users


@route.post("/", response_model=CustomerUsers)
def create_user(user: CustomerUsersCreate, session: SessionDep):
    user = CustomerUsers(**user.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@route.post("/user-verification")
def validate_user(mobile_no, session: SessionDep):
    user = session.query(CustomerUsers).filter(CustomerUsers.mobile_no == mobile_no).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    return {"detail": "Ok"}


@route.post("/otp-verification")
def validate_otp(otp: int, session: SessionDep):
    if otp != 1234:
        raise HTTPException(status_code=403, detail="Invalid OTP")
    return {"detail": "Ok"}


# Saved Address

@route.post("/address", response_model=SavedAddress)
def create_user(address: SavedAddressCreate, session: SessionDep):
    addr = SavedAddress(**address.model_dump())
    session.add(addr)
    session.commit()
    session.refresh(addr)
    return addr


@route.get("/address")
def user_address(user_id: int, session: SessionDep) -> list[SavedAddress]:
    addr = session.query(SavedAddress).filter(SavedAddress.user_id == user_id).all()
    if not addr:
        raise HTTPException(status_code=404, detail="No saved address found for user")
    return addr


@route.post("/partner/user", response_model=PartnerUsers)
def create_partner_user(user: PartnerUsersCreate, session: SessionDep):
    user = PartnerUsers(**user.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@route.get("/partner/{partner_id}")
def fetch_partner(partner_id: int, session: SessionDep) -> PartnerUsers:
    partner = session.query(PartnerUsers).filter(PartnerUsers.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner Not found")
    return partner


@route.post("/partner/approval/{partner_id}")
def fetch_partner(partner_id: int, approval_status: str, session: SessionDep) -> PartnerUsers:
    partner = session.query(PartnerUsers).filter(PartnerUsers.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner Not found")

    partner.approval_status = approval_status
    session.add(partner)
    session.commit()
    session.refresh(partner)
    return partner


@route.get("/partner")
def read_partners(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=20)] = 20,
) -> list[PartnerUsers]:
    partners = session.query(PartnerUsers).offset(offset).limit(limit).all()
    return partners
