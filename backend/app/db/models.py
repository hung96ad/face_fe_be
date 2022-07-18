from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('room.id'))
    name = Column(String, index=True, nullable=False)

class RoomTree(Base):
    __tablename__ = "room_tree_view"

    id = Column(Integer,primary_key=True)
    parent_id = Column(Integer,)
    name = Column(String)
    type_room = Column(Integer)
    order_sequence = Column(String)
    parent_name = Column(String)