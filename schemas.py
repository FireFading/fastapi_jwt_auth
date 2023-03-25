from pydantic import BaseModel


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
