from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.model.camera import Camera
from app.db.schema import camera as schemas_camera
from app.db.curd.room import get_query, query_count


def get_camera(db: Session, camera_id: int):
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera


def get_camera_by_name(
        db: Session, q: str, filter:dict = {}, skip: int = 0, limit: int = 100, order_by: list = []
    ) -> t.Tuple[int, t.List[schemas_camera.Camera]]:
    query = db.query(Camera)
    if q:
        query = query.filter(Camera.name.ilike(f"%{q}%"))
    query = get_query(query, filter, order_by, Camera)
    count = query_count(query)
    query = query.offset(skip).limit(limit)
    return count, query.all()


def create_camera(db: Session, camera: schemas_camera.CameraCreate):
    db_camera = Camera(
        id_room=camera.id_room,
        rtsp=camera.rtsp,
        name=camera.name,
        status=camera.status
    )
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


def delete_camera(db: Session, camera_id: int):
    camera = get_camera(db, camera_id)
    if not camera:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Camera not found")
    db.delete(camera)
    db.commit()
    return camera


def edit_camera(
    db: Session, camera_id: int, camera: schemas_camera.CameraEdit
) -> schemas_camera.Camera:
    db_camera = get_camera(db, camera_id)
    if not db_camera:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Camera not found")
    update_data = camera.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_camera, key, value)

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera
