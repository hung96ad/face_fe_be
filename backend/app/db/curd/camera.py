from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.model.camera import Camera
from app.db.schema import camera as schemas_camera
from app.db.curd.room import get_query, query_count
import aiohttp
import asyncio
from app.core import config


def get_camera(db: Session, camera_id: int) -> Camera:
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera


def get_camera_by_name(
    db: Session, q: str, filter: dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
) -> t.Tuple[int, t.List[schemas_camera.Camera]]:
    query = db.query(Camera)
    if q:
        query = query.filter(Camera.name.ilike(f"%{q}%"))
    query = get_query(query, filter, order_by, Camera)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def get_all_cameras(db: Session) -> t.List[schemas_camera.Camera]:
    query = db.query(Camera)
    return query.all()

async def create_camera(db: Session, camera: schemas_camera.CameraCreate):
    db_camera = Camera(
        id_room=camera.id_room,
        rtsp=camera.rtsp,
        name=camera.name,
        status=camera.status
    )
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    result_call = await update_camera_to_ai_server(db_camera.service_type, db_camera.rtsp, db_camera.id)
    print(result_call)
    return db_camera


def delete_camera(db: Session, camera_id: int):
    camera = get_camera(db, camera_id)
    if not camera:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Camera not found")
    db.delete(camera)
    db.commit()
    return camera


async def edit_camera(
    db: Session, camera: schemas_camera.CameraEdit
) -> schemas_camera.Camera:
    db_camera = get_camera(db, camera.id)
    if not db_camera:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Camera not found")
    update_data = camera.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_camera, key, value)

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    result_call = await update_camera_to_ai_server(db_camera.service_type, db_camera.rtsp, db_camera.id)
    print(result_call)
    return db_camera

async def update_camera_to_ai_server(service_type="", rtsp='', camera_id=''):
    json_data = {
        "service_type": service_type,
        "rtsp": rtsp,
        "camera_id": camera_id
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{config.HOST_BE_AI}{config.ADD_CAMERA}",
                                     json=json_data)  as resp:
            
            res = await resp.json()
            return res