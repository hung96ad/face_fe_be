from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    parent_id: int = None
    name: str = None
    type_room: int = None


class RoomOut(RoomBase):
    pass


class RoomCreate(RoomBase):
    class Config:
        orm_mode = True


class RoomEdit(RoomBase):
    class Config:
        orm_mode = True


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

class RoomTree(RoomBase):
    id: int
    order_sequence: str
    parent_name: str
    full_path: str

    class Config:
        orm_mode = True
