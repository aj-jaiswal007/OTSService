import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = os.getenv("BASE_URL", "")
    MASTER_USERNAME: str = os.getenv("MASTER_USERNAME", "")
    MASTER_PASSWORD: str = os.getenv("MASTER_PASSWORD", "")


@lru_cache()
def get_settings():
    return Settings()
