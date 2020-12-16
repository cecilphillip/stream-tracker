from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    mongo_database_name: str     
    mongo_connection_string: str

    class Config:
        env_file = "local.env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()