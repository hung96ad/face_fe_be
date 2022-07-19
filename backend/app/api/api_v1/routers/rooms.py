from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.curd.room import (
    get_room_by_name,
    create_room,
    delete_room,
    edit_room,
    get_room_view
)
from app.db.schema.room import RoomCreate, RoomEdit, Room, RoomTree
from app.db.schemas import QueryParams

rooms_router = r = APIRouter()


@r.get(
    "/rooms/{room_id}",
    response_model=Room,
    response_model_exclude_none=True,
)
async def room_details(
    request: Request,
    room_id: int,
    db=Depends(get_db)
):
    """
    Get any room details
    """
    room = get_room_view(db, room_id)
    return room



@r.get(
    "/rooms",
    response_model=t.List[RoomTree],
    response_model_exclude_none=True,
)
async def rooms_by_name(
    response: Response,
    filter: t.Union[str, None] = {},
    range: t.Union[str, None] = None,
    sort: t.Union[str, None] = None,
    db=Depends(get_db)
):
    """
    Get any rooms by name
    """
    query_params = QueryParams(filter=filter, range=range, sort=sort)
    q, skip, limit, filter, sort, range = query_params.get_query_params("q")  
    count, rooms = get_room_by_name(db, q=q, filter=filter, skip=skip, limit=limit, order_by=sort)
    response.headers["Content-Range"] = f"items {range[0]}-{range[1]}/{count}"
    return rooms


@r.post("/rooms", response_model=Room, response_model_exclude_none=True)
async def room_create(
    request: Request,
    room: RoomCreate,
    db=Depends(get_db),
):
    """
    Create a new room
    """
    return create_room(db, room)


@r.put(
    "/rooms/{room_id}", response_model=Room, response_model_exclude_none=True
)
async def room_edit(
    request: Request,
    room_id: int,
    room: RoomEdit,
    db=Depends(get_db),
):
    """
    Update existing room
    """
    return edit_room(db, room_id, room)


@r.delete(
    "/rooms/{room_id}", response_model=Room, response_model_exclude_none=True
)
async def room_delete(
    request: Request,
    room_id: int,
    db=Depends(get_db),
):
    """
    Delete existing room
    """
    return delete_room(db, room_id)
