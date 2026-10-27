"""CRUD controller for the sandwiches database table."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ._helpers import commit_or_conflict


def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(**sandwich.model_dump())
    db.add(db_sandwich)
    commit_or_conflict(db)
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()


def update(db: Session, sandwich_id: int, sandwich):
    db_sandwich = read_one(db, sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwiches record not found")
    for key, value in sandwich.model_dump(exclude_unset=True).items():
        setattr(db_sandwich, key, value)
    commit_or_conflict(db)
    db.refresh(db_sandwich)
    return db_sandwich


def delete(db: Session, sandwich_id: int):
    db_sandwich = read_one(db, sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwiches record not found")
    db.delete(db_sandwich)
    commit_or_conflict(db)
