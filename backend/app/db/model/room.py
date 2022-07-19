from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.session import Base

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