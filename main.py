from typing import List

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "601bac40d267c5c4a847e5f3d7f499e39e08da2bf446fc336c81a944c6e3202d"
    )


@AuthJWT.load_config
def get_config():
    return Settings()


class User(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password",
                "email": "email@example.com",
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password",
            }
        }


users = []


@app.post("/signup", status_code=201)
def create_user(user: User):
    new_user = {
        "username": user.username,
        "password": user.password,
        "email": user.email,
    }
    users.append(new_user)

    return new_user


@app.get("/users", response_model=List[User])
def get_users():
    return users


@app.post("/login")
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    for u in users:
        if u.get("username") == user.username and u.get("password") == user.password:
            access_token = Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)

            return {"access_token": access_token, "refresh_token": refresh_token}
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/protected")
def get_logged_in_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()

    return {"current_user": current_user}


@app.get("/new_token")
def create_new_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return {"new access token": access_token}
