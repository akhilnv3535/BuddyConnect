from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from core.db import SessionDep
from route.models import Category, CategoryCreate, SubCategory, SubCategoryCreate, Services, ServicesCreate

cat_route = APIRouter(prefix="/cat", tags=["Categories"])


# Service's API
@cat_route.post("/services/", response_model=Services)
def create_service(service: ServicesCreate, session: SessionDep):
    service = Services(**service.model_dump())
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@cat_route.get("/services")
def read_services(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[Services]:
    services = session.query(Services).offset(offset).limit(limit).all()
    return services


@cat_route.get("/services/{service_id}")
def read_service(service_id: int, session: SessionDep) -> Services:
    service = session.get(Services, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Hero not found")
    return service


@cat_route.delete("/services/{service_id}")
def delete_service(service_id: int, session: SessionDep):
    service = session.get(Services, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(service)
    session.commit()
    return {"ok": True}


# Category
@cat_route.post("/category", response_model=Category)
def create_category(category: CategoryCreate, session: SessionDep):
    cat = Category(**category.model_dump())
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@cat_route.get("/category")
def read_categorys(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[Category]:
    categories = session.query(Category).offset(offset).limit(limit).all()
    return categories


@cat_route.get("/category/{cat_id}")
def read_category(cat_id: int, session: SessionDep) -> Category:
    category = session.get(Category, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Hero not found")
    return category


# @cat_route.delete("/category/{cat_id}")
# def delete_category(cat_id: int, session: SessionDep):
#     category = session.get(Category, cat_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(category)
#     session.commit()
#     return {"ok": True}


# Sub Category
@cat_route.post("/sub-category", response_model=SubCategory, tags=["Sub Categories"])
def create_sub_category(sub_category: SubCategoryCreate, session: SessionDep):
    sub_cat = SubCategory(**sub_category.model_dump())
    session.add(sub_cat)
    session.commit()
    session.refresh(sub_cat)
    return sub_cat


@cat_route.get("/sub-category", tags=["Sub Categories"])
def read_sub_categorys(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[SubCategory]:
    sub_categories = session.query(SubCategory).offset(offset).limit(limit).all()
    return sub_categories


@cat_route.get("/sub-category/{sub_cat_id}", tags=["Sub Categories"])
def read_sub_category(sub_cat_id: int, session: SessionDep) -> SubCategory:
    sub_category = session.get(SubCategory, sub_cat_id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub Category not found")
    return sub_category

# @cat_route.delete("/sub-category/{sub_cat_id}", tags=["Sub Categories"])
# def delete_sub_category(sub_cat_id: int, session: SessionDep):
#     sub_category = session.get(SubCategory, sub_cat_id)
#     if not sub_category:
#         raise HTTPException(status_code=404, detail="Sub Category not found")
#     session.delete(sub_category)
#     session.commit()
#     return {"ok": True}
