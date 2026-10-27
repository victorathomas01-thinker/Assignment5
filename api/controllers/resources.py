"""CRUD controller for the resources database table."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import models
from ._helpers import commit_or_conflict


def create(db: Session, resource):
    db_resource = models.Resource(**resource.model_dump())
    db.add(db_resource)
    commit_or_conflict(db)
    db.refresh(db_resource)
    return db_resource


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


def update(db: Session, resource_id: int, resource):
    db_resource = read_one(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resources record not found")
    for key, value in resource.model_dump(exclude_unset=True).items():
        setattr(db_resource, key, value)
    commit_or_conflict(db)
    db.refresh(db_resource)
    return db_resource


def delete(db: Session, resource_id: int):
    db_resource = read_one(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resources record not found")
    db.delete(db_resource)
    commit_or_conflict(db)
