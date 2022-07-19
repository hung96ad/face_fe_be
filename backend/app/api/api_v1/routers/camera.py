from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.crud_camera import (
    get_camera_by_name,
    create_camera,
    delete_camera,
    edit_camera,
    get_camera_view
)
from app.db.schemas_camera import CameraCreate, CameraEdit, Camera, CameraTree
from app.db.schemas import QueryParams

cameras_router = r = APIRouter()


@r.get(
    "/cameras/{camera_id}",
    response_model=Camera,
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
    camera = get_camera_view(db, camera_id)
    return camera



@r.get(
    "/cameras",
    response_model=t.List[CameraTree],
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
    return create_camera(db, camera)


@r.put(
    "/cameras/{camera_id}", response_model=Camera, response_model_exclude_none=True
)
async def camera_edit(
    request: Request,
    camera_id: int,
    camera: CameraEdit,
    db=Depends(get_db),
):
    """
    Update existing camera
    """
    return edit_camera(db, camera_id, camera)


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
