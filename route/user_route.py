from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from route.models import CustomerUsers, CustomerUsersCreate

route = APIRouter(prefix="/user", tags=["Users"])


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
