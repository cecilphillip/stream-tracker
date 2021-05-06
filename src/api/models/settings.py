from pydantic import BaseSettings
from functools import lru_cache

from utils import get_project_rootdir

class Settings(BaseSettings):
    project_name: str
    log_level: str
    mongo_database_name: str
    mongo_connection_string: str

    class Config:
        env_file = f"{get_project_rootdir()}/local.env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
