from pydantic import BaseModel
from typing import Optional

class CameraBase(BaseModel):
    id_room: int
    name: Optional[str]
    status: Optional[bool]
    service_type: Optional[str]


class CameraOut(CameraBase):
    id: int
    rtsp: str
    class Config:
        orm_mode = True

class CameraCreate(CameraBase):
    rtsp: str
    class Config:
        orm_mode = True


class CameraEdit(CameraBase):
    id: int
    rtsp: str
    class Config:
        orm_mode = True


class Camera(CameraBase):
    id: int

    class Config:
        orm_mode = True

class CamerasGet(BaseModel):
    id: int
    rtsp: Optional[str]
    class Config:
        orm_mode = True