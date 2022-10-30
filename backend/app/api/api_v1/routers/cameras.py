from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.curd.camera import (
    get_camera_by_name,
    create_camera,
    delete_camera,
    edit_camera,
    get_camera,
    get_all_cameras
)
from app.db.schema.camera import CameraCreate, CameraEdit, CameraOut, Camera, CamerasGet
from app.db.schemas import QueryParams

cameras_router = r = APIRouter()


@r.get(
    "/cameras/{camera_id}",
    response_model=CameraOut,
    response_model_exclude_none=True,
)
async def camera_details(
    request: Request,
    camera_id: int,
    db=Depends(get_db)
):
    """
    Get any camera details
    """
    camera = get_camera(db, camera_id)
    return camera



@r.get(
    "/cameras",
    response_model=t.List[Camera],
    response_model_exclude_none=True,
)
async def cameras_by_name(
    response: Response,
    filter: t.Union[str, None] = {},
    range: t.Union[str, None] = None,
    sort: t.Union[str, None] = None,
    db=Depends(get_db)
):
    """
    Get any cameras by name
    """
    query_params = QueryParams(filter=filter, range=range, sort=sort)
    q, skip, limit, filter, sort, range = query_params.get_query_params("q")  
    count, cameras = get_camera_by_name(db, q=q, filter=filter, skip=skip, limit=limit, order_by=sort)
    response.headers["Content-Range"] = f"items {range[0]}-{range[1]}/{count}"
    return cameras


@r.post("/cameras", response_model=Camera, response_model_exclude_none=True)
async def camera_create(
    request: Request,
    camera: CameraCreate,
    db=Depends(get_db),
):
    """
    Create a new camera
    """
    return await create_camera(db, camera)


@r.put(
    "/cameras", response_model=Camera, response_model_exclude_none=True
)
async def camera_edit(
    request: Request,
    camera: CameraEdit,
    db=Depends(get_db),
):
    """
    Update existing camera
    """
    return await edit_camera(db, camera)


@r.delete(
    "/cameras/{camera_id}", response_model=Camera, response_model_exclude_none=True
)
async def camera_delete(
    request: Request,
    camera_id: int,
    db=Depends(get_db),
):
    """
    Delete existing camera
    """
    return delete_camera(db, camera_id)


@r.get(
    "/cameras_get",
    response_model=t.List[CamerasGet],
    response_model_exclude_none=True,
)
async def cameras_get(
    db=Depends(get_db)
):
    """
    Get all cameras
    """
    cameras = get_all_cameras(db)
    return cameras