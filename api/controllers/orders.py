"""CRUD for existing Orders example from the instructor's starter."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ._helpers import commit_or_conflict


def create(db: Session, order):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    commit_or_conflict(db)
    db.refresh(db_order)
    return db_order


def read_all(db: Session):
    return db.query(models.Order).all()


def read_one(db: Session, order_id):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update(db: Session, order_id, order):
    db_order = read_one(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)
    commit_or_conflict(db)
    db.refresh(db_order)
    return db_order


def delete(db: Session, order_id):
    db_order = read_one(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    commit_or_conflict(db)
