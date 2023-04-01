import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import router
from app.settings import Settings
from fastapi_jwt_auth import AuthJWT


@AuthJWT.load_config
def get_config():
    return Settings()


app = FastAPI()


app.include_router(router)
add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
