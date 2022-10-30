from xmlrpc.client import Boolean
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.model.face import Face, FaceImage
from app.db.schema import face as schemas_face
from app.db.curd.room import get_query, query_count
from app.core import config
import os
from datetime import datetime
import aiohttp
import asyncio

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


def get_face_images_by_face_id(
    db: Session, filter: dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
) -> t.Tuple[int, t.List[schemas_face.FaceImagesOut]]:
    query = db.query(FaceImage)
    query = get_query(query, filter, order_by, FaceImage)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def get_face_by_name(
    db: Session, q: str, filter: dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
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


def save_face_image(db: Session, face_id: int, filename: str, contents: bytes) -> FaceImage:
    path_folder = f"{config.PATH_STATIC}/{face_id}"
    os.makedirs(path_folder, exist_ok=True)
    file_path = f"{path_folder}/{filename}"
    with open(file_path, 'wb') as f:
        f.write(contents)
    path = f"{config.STATIC_API}/{face_id}/{filename}"
    face_image = FaceImage(id_face=face_id,
                           path=path,
                           local_path=file_path,
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

async def get_face_logs(keep_unknow:bool = True):
    json_data = config.DEFAULT_JSON_FACE
    json_data['keep_unknow'] = keep_unknow
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{config.HOST_BE_AI}{config.FACE_LOGS}",
                                     json=json_data)  as resp:
            
            results = await resp.json()
            dt = []
            if 'data' in results:
                for re in results['data']:
                    dt.append({
                        "id": re['_id'],
                        "time_created": datetime.fromtimestamp(re['_source']['time_created']),
                        "camera_id": re['_source']['camera_id'],
                        "face_id": re['_source']['face_id'],
                        "face_url": re['_source']['face_url']
                    })
            return dt
        
async def insert_face_ai(face_images: FaceImage):
    url = f"{config.HOST_BE_AI}{config.ADD_FACE}"
    files = {'file': open(face_images.local_path, 'rb'),
        "user_id": f"{face_images.id_face}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=files)  as resp:
            results = await resp.json()
            print(f"insert_face_ai {results}")
        
async def upload_image(file, db, face_id):
    contents = await file.read()
    face_image = save_face_image(db, face_id, file.filename, contents)
    await insert_face_ai(face_image)
