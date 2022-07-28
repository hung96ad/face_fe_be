from fastapi import APIRouter, Request, Depends, Response, File, Form, UploadFile
import typing as t

from app.db.session import get_db
from app.db.curd.face import (
    get_face_by_name,
    create_face,
    delete_face,
    edit_face,
    get_face,
    save_face_image,
    delete_face_images,
    get_face_images_by_face_id
)
from app.db.schema.face import FaceEdit, FaceOut, FaceCreate, FaceImagesOut
from app.db.schemas import QueryParams

faces_router = r = APIRouter()


@r.get(
    "/faces/{face_id}",
    response_model=FaceOut,
    response_model_exclude_none=True,
)
async def face_details(
    request: Request,
    face_id: int,
    db=Depends(get_db)
):
    """
    Get any face details
    """
    face = get_face(db, face_id)
    return face


@r.get(
    "/faces",
    response_model=t.List[FaceOut],
    response_model_exclude_none=True,
)
async def faces_by_name(
    response: Response,
    filter: t.Union[str, None] = {},
    range: t.Union[str, None] = None,
    sort: t.Union[str, None] = None,
    db=Depends(get_db)
):
    """
    Get any faces by name
    """
    query_params = QueryParams(filter=filter, range=range, sort=sort)
    q, skip, limit, filter, sort, range = query_params.get_query_params("q")
    count, faces = get_face_by_name(
        db, q=q, filter=filter, skip=skip, limit=limit, order_by=sort)
    response.headers["Content-Range"] = f"items {range[0]}-{range[1]}/{count}"
    return faces


@r.post("/faces", response_model=FaceOut, response_model_exclude_none=True)
async def face_create(
    request: Request,
    id_room: int = Form(default=None),
    name: str = Form(default=None),
    status: bool = Form(default=True),
    file: UploadFile = File(default=None),
    db=Depends(get_db),
):
    """
    Create a new face
    """
    face = FaceCreate(id_room=id_room, name=name, status=status)
    db_face = create_face(db, face)
    if file:
        contents = await file.read()
        _ = save_face_image(db, db_face.id, file.filename, contents)
    return db_face


@r.put(
    "/faces", response_model=FaceOut, response_model_exclude_none=True
)
async def face_edit(
    request: Request,
    id: int = Form(default=None),
    id_room: int = Form(default=None),
    name: str = Form(default=None),
    status: bool = Form(default=True),
    file: UploadFile = File(default=None),
    db=Depends(get_db),
):
    """
    Update existing face
    """
    face = FaceEdit(id=id, id_room=id_room, name=name, status=status)
    if file:
        contents = await file.read()
        _ = save_face_image(db, id, file.filename, contents)
    return edit_face(db, id, face)


@r.delete(
    "/faces/{face_id}", response_model=FaceOut, response_model_exclude_none=True
)
async def face_delete(
    request: Request,
    face_id: int,
    db=Depends(get_db),
):
    """
    Delete existing face
    """
    return delete_face(db, face_id)


@r.post("/face_images", response_model=FaceImagesOut, response_model_exclude_none=True)
async def face_image_create(
    request: Request,
    face_id: int = Form(default=None),
    file: UploadFile = File(default=None),
    db=Depends(get_db),
):
    """
    Create a new face image
    """
    contents = await file.read()
    face_image = save_face_image(db, face_id, file.filename, contents)
    return face_image


@r.delete(
    "/face_images/{face_images_id}", response_model=FaceImagesOut, response_model_exclude_none=True
)
async def face_images_delete(
    request: Request,
    face_images_id: int,
    db=Depends(get_db),
):
    """
    Delete existing face images
    """
    return delete_face_images(db, face_images_id)


@r.get("/face_images",
       response_model=t.List[FaceImagesOut],
       response_model_exclude_none=True)
async def get_face_image_by_face_id(
    response: Response,
    filter: t.Union[str, None] = {},
    range: t.Union[str, None] = None,
    sort: t.Union[str, None] = None,
    db=Depends(get_db)
):
    """
    Get list face images by face id
    """
    query_params = QueryParams(filter=filter, range=range, sort=sort)
    _, skip, limit, filter, sort, range = query_params.get_query_params("q")
    count, face_images = get_face_images_by_face_id(
        db, filter=filter, skip=skip, limit=limit, order_by=sort)
    response.headers["Content-Range"] = f"items {range[0]}-{range[1]}/{count}"
    return face_images
