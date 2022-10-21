from pydantic import BaseModel
from typing import List, Optional

class ContainerBase(BaseModel):
    container_id: str
    time_checked: Optional[str]
    status: Optional[int]
    port: Optional[str]
    server_ip: Optional[str]
    service_type: Optional[str]
    cameras_id: Optional[List[int]]
    class Config:
        orm_mode = True