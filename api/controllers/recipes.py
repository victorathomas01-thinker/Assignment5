"""CRUD controller for the recipes database table."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ._helpers import commit_or_conflict


def create(db: Session, recipe):
    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    commit_or_conflict(db)
    db.refresh(db_recipe)
    return db_recipe


def read_all(db: Session):
    return db.query(models.Recipe).all()


def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def update(db: Session, recipe_id: int, recipe):
    db_recipe = read_one(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipes record not found")
    for key, value in recipe.model_dump(exclude_unset=True).items():
        setattr(db_recipe, key, value)
    commit_or_conflict(db)
    db.refresh(db_recipe)
    return db_recipe


def delete(db: Session, recipe_id: int):
    db_recipe = read_one(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipes record not found")
    db.delete(db_recipe)
    commit_or_conflict(db)
