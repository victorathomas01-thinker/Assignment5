"""CRUD controller for the order_details database table."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ._helpers import commit_or_conflict


def create(db: Session, order_detail):
    db_order_detail = models.OrderDetail(**order_detail.model_dump())
    db.add(db_order_detail)
    commit_or_conflict(db)
    db.refresh(db_order_detail)
    return db_order_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()


def update(db: Session, order_detail_id: int, order_detail):
    db_order_detail = read_one(db, order_detail_id)
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="Order Details record not found")
    for key, value in order_detail.model_dump(exclude_unset=True).items():
        setattr(db_order_detail, key, value)
    commit_or_conflict(db)
    db.refresh(db_order_detail)
    return db_order_detail


def delete(db: Session, order_detail_id: int):
    db_order_detail = read_one(db, order_detail_id)
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="Order Details record not found")
    db.delete(db_order_detail)
    commit_or_conflict(db)
