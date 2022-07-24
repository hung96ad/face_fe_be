from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.model.face import Face, FaceImage
from app.db.schema import face as schemas_face
from app.db.curd.room import get_query, query_count
from app.core import config
import os


def get_face(db: Session, face_id: int):
    face = db.query(Face).filter(Face.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")
    return face

def get_face_images(db: Session, face_id: int):
    face = db.query(FaceImage).filter(FaceImage.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face image not found")
    return face

def get_face_by_name(
        db: Session, q: str, filter:dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
    ) -> t.Tuple[int, t.List[schemas_face.FaceOut]]:
    query = db.query(Face)
    if q:
        query = query.filter(Face.name.ilike(f"%{q}%"))
    query = get_query(query, filter, order_by, Face)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def create_face(db: Session, face: schemas_face.FaceCreate):
    db_face = Face(
        id_room=face.id_room,
        name=face.name,
        status=face.status
    )
    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face


def delete_face(db: Session, face_id: int):
    face = get_face(db, face_id)
    if not face:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Face not found")
    db.delete(face)
    db.commit()
    return face


def edit_face(
    db: Session, face_id: int, face: schemas_face.FaceEdit
) -> schemas_face.FaceOut:
    db_face = get_face(db, face_id)
    if not db_face:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Face not found")
    update_data = face.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_face, key, value)

    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face


def save_face_image(db: Session, face_id:int, filename:str, contents:bytes):
    path_folder = f"{config.PATH_STATIC}/{face_id}"
    os.makedirs(path_folder, exist_ok=True)
    file_path = f"{path_folder}/{filename}"
    with open(file_path, 'wb') as f:
        f.write(contents)
    path = f"{config.STATIC_API}/{face_id}/{filename}"
    face_image = FaceImage(id_face=face_id,
        path = path,
        status=True)
    db.add(face_image)
    db.commit()
    db.refresh(face_image)
    return face_image

def delete_face_images(db: Session, face_id: int):
    face = get_face_images(db, face_id)
    if not face:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Face not found")
    db.delete(face)
    db.commit()
    return face