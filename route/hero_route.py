# from typing import Annotated
#
# from fastapi import APIRouter
# from fastapi import HTTPException, Query
#
# from core.db import SessionDep
# from route.models import Hero
# from route.schemas import HeroSchema
#
# route = APIRouter(prefix="/hero", tags=['Hero'])
#
#
# @route.post("/heroes/")
# def create_hero(hero: HeroSchema, session: SessionDep) -> Hero:
#     hero = Hero(**hero.model_dump())
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero
#
#
# @route.get("/heroes/")
# def read_heroes(
#         session: SessionDep,
#         offset: int = 0,
#         limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[Hero]:
#     heroes = session.query(Hero).offset(offset).limit(limit).all()
#     # heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes
#
#
# @route.get("/heroes/{hero_id}")
# def read_hero(hero_id: int, session: SessionDep) -> Hero:
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero
#
#
# @route.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}
