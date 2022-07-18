from fastapi import HTTPException, status
from sqlalchemy import text, func, literal_column
from sqlalchemy.orm import Session
import typing as t
from . import models, schemas_room


def query_count(query):
    ONE = literal_column("1")
    counter = query.statement.with_only_columns([func.count(ONE)])
    counter = counter.order_by(None)
    return query.session.execute(counter).scalar()

def get_query(query, filter, order_by, table):
    query = query.filter(
        *[
            getattr(table, k).in_(v)
            if isinstance(v, list)
            else getattr(table, k) == v
            for k, v in filter.items()
        ])
    for idx in range(0, len(order_by), 2):
        query = query.order_by(text(f"{order_by[idx]} {order_by[idx+1]}"))
    return query

def get_room_view(db: Session, room_id: int):
    room = db.query(models.RoomTree).filter(models.RoomTree.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

def get_room(db: Session, room_id: int):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def get_room_by_name(
        db: Session, q: str, filter:dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
    ) -> t.Tuple[int, t.List[schemas_room.RoomTree]]:
    query = db.query(models.RoomTree)
    if q:
        query = query.filter(models.RoomTree.name.ilike(f"%{q}%"))
    query = get_query(query, filter, order_by, models.RoomTree)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def create_room(db: Session, room: schemas_room.RoomCreate):
    db_room = models.Room(
        parent_id=room.parent_id,
        name=room.name
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Room not found")
    db.delete(room)
    db.commit()
    return room


def edit_room(
    db: Session, room_id: int, room: schemas_room.RoomEdit
) -> schemas_room.Room:
    db_room = get_room(db, room_id)
    if not db_room:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Room not found")
    update_data = room.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_room, key, value)

    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
