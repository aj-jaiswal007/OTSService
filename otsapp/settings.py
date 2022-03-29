import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = os.getenv("BASE_URL", "")


@lru_cache()
def get_settings():
    return Settings()
