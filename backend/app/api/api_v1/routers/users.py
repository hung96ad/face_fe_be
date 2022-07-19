from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.curd.user import (
    get_users,
    get_user,
    create_user,
    delete_user,
    edit_user,
)
from app.db.schema.user import UserCreate, UserEdit, User
from app.core.auth import get_current_active_user, get_current_active_superuser
from app.db.schemas import QueryParams

users_router = r = APIRouter()


@r.get(
    "/users",
    response_model=t.List[User],
    response_model_exclude_none=True,
)
async def users_list(
    response: Response,
    filter: t.Union[str, None] = {},
    range: t.Union[str, None] = None,
    sort: t.Union[str, None] = None,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get all users
    """
    query_params = QueryParams(filter=filter, range=range, sort=sort)
    q, skip, limit, filter, sort, range = query_params.get_query_params("q")
    count, users = get_users(db, q=q, filter=filter, skip=skip, limit=limit, order_by=sort)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"items {range[0]}-{range[1]}/{count}"
    return users


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """
    Get own user
    """
    return current_user


@r.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True,
)
async def user_details(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    user = get_user(db, user_id)
    return user
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/users", response_model=User, response_model_exclude_none=True)
async def user_create(
    request: Request,
    user: UserCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Create a new user
    """
    return create_user(db, user)


@r.put(
    "/users/{user_id}", response_model=User, response_model_exclude_none=True
)
async def user_edit(
    request: Request,
    user_id: int,
    user: UserEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    return edit_user(db, user_id, user)


@r.delete(
    "/users/{user_id}", response_model=User, response_model_exclude_none=True
)
async def user_delete(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    return delete_user(db, user_id)
