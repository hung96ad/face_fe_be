#!/usr/bin/env python3

from app.db.session import get_db
from app.db.curd.user import create_user
from app.db.schema.user import UserCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="admin@dev-fastapi-react.com",
            password="password",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser admin@dev-fastapi-react.com")
    init()
    print("Superuser created")
