from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from app.db.session import Base

class Face(Base):
    __tablename__ = "face"

    id = Column(Integer, primary_key=True, index=True)
    id_room = Column(Integer, ForeignKey('room.id'))
    name = Column(String, index=True, nullable=False)
    status = Column(Boolean, default=True)

class FaceImage(Base):
    __tablename__ = "face_images"

    id = Column(Integer, primary_key=True, index=True)
    id_face = Column(Integer, ForeignKey('face.id'))
    path = Column(String)
    local_path = Column(String)
    status = Column(Boolean, default=True)
