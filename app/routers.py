from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import User, UserLogin
from app.utils import get_hashed_password, verify_password
from fastapi_jwt_auth import AuthJWT

router = APIRouter(prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}})

users: list = []


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[User],
    summary="get all registered users that",
)
def get_users(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e

    return users


@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="register user")
def register_user(user: User):
    new_user = {
        "username": user.username,
        "password": get_hashed_password(password=user.password),
        "email": user.email,
    }
    users.append(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK, summary="login user")
def login(user: UserLogin, authorize: AuthJWT = Depends()):
    for u in users:
        if u.get("username") == user.username and verify_password(
            password=user.password, hashed_password=u.get("password")
        ):
            access_token = authorize.create_access_token(subject=user.username)
            refresh_token = authorize.create_refresh_token(subject=user.username)

            return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


@router.get(
    "/protected",
    status_code=status.HTTP_200_OK,
    summary="get current log-in user by JWT access token",
)
def get_logged_in_user(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e

    current_user = authorize.get_jwt_subject()

    return {"current_user": current_user}


@router.get(
    "/new_token",
    status_code=status.HTTP_200_OK,
    summary="exchange refresh token to new access",
)
def create_new_token(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e

    current_user = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=current_user)

    return {"new_access_token": access_token}
