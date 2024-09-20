import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DB_CHARSET = "utf8mb4"


class Env(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

env = Env()