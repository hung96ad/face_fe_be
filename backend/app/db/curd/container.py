from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.model.container import Container
from app.db.schema.container import ContainerBase
from app.db.curd.room import get_query, query_count


def update_container(db: Session, container_base: ContainerBase):
    container = db.query(Container).filter(Container.container_id == container_base.container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {
        "status": "available"
        }

def get_all_containers(db: Session) -> t.List[ContainerBase]:
    query = db.query(Container)
    return query.all()

