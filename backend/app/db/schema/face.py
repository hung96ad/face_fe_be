from pydantic import BaseModel
from typing import Optional

class FaceBase(BaseModel):
    id_room: Optional[int]
    name: Optional[str]
    status: Optional[bool]


class FaceOut(FaceBase):
    id: int
    class Config:
        orm_mode = True

class FaceCreate(FaceBase):
    class Config:
        orm_mode = True


class FaceEdit(FaceBase):
    id: int
    class Config:
        orm_mode = True


class FaceImagesBase(BaseModel):
    id_face: int
    path: str
    status: bool

class FaceImagesCreate(FaceImagesBase):
    class Config:
        orm_mode = True


class FaceImagesEdit(FaceImagesBase):
    id: int
    class Config:
        orm_mode = True

class FaceImagesOut(FaceImagesBase):
    id: int
    class Config:
        orm_mode = True