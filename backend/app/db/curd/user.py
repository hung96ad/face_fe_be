from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from app.db.model.user import User
from app.db.schema import user as schemas_user
from app.core.security import get_password_hash
from .room import get_query, query_count


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas_user.UserBase:
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session, q: str, filter:dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
) -> t.Union[int , t.List[schemas_user.UserOut]]:
    query = db.query(User)
    if q:
        query = query.filter(User.email.ilike(f"%{q}%"))
    query = get_query(query, filter, order_by, User)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def create_user(db: Session, user: schemas_user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas_user.UserEdit
) -> schemas_user.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
