from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(dotenv_path="./")


class Settings(BaseSettings):
    authjwt_secret_key: str = Field(env="AUTHJWT_SECRET_KEY")

    access_token_expires: int = Field(env="ACCESS_TOKEN_EXPIRES")
    refresh_token_expires: int = Field(env="REFRESH_TOKEN_EXPIRES")

    class Config:
        env_file = "./.env"
