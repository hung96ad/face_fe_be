import os

PROJECT_NAME = "dev-fastapi-react"

# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/postgres"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

API_V1_STR = "/api/v1"

PATH_STATIC = "./app/static"
STATIC_API = "/static_be"
HOST_BE_AI = "http://192.168.1.86:8106"

ADD_FACE = "/api/v1/insert"
FACE_LOGS = "/api/v1/logs"
ADD_CAMERA = "/api/v1/add_camera"

DEFAULT_JSON_FACE = {
    "from_time": 1,
    "to_time": 0,
    "size_": 50,
    "cameras_id": [],
    "faces_id": [],
    "sort_by": "desc"
}
