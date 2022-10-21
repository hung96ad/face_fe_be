from matplotlib import container
from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.db.session import Base

class Container(Base):
    __tablename__ = "container"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(String, unique=True)
    cameras_id = Column(Integer)
    status = Column(Integer)
    port = Column(String)
    server_ip = Column(String)
    service_type = Column(Integer)
    time_checked = Column(TIMESTAMP)

