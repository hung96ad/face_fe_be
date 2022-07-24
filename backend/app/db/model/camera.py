from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from app.db.session import Base

class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, index=True)
    id_room = Column(Integer, ForeignKey('room.id'))
    name = Column(String, index=True, nullable=False)
    rtsp = Column(String, nullable=False)
    status = Column(Boolean, default=True)
