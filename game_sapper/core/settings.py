import os

from pydantic import BaseModel, BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Postgres(BaseModel):
    db: str = ""
    host: str = ""
    port: int = 5432
    password: str = ""
    user: str = ""
    db_schema: str = ""

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Apispec(BaseModel):
    title: str = "Документация"
    swagger_path: str = "/"


class VK(BaseModel):
    token: str = ""
    group_id: str = ""


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8004
    logging_level: str = "INFO"
    logging_guru: bool = True
    traceback: bool = False

    postgres: Postgres = Postgres()
    apispec: Apispec = Apispec()
    vk: VK = VK()

    class Config:
        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env"
        enf_file_encoding = "utf-8"
