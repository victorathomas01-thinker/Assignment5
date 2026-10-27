"""Shared database error handling for all CRUD controllers."""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def commit_or_conflict(db):
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Database conflict: duplicate value or invalid/referenced related record",
        ) from error
