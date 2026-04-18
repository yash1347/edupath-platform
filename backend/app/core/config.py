import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str
    api_prefix: str
    database_url: str
    cors_origins: list[str]


@lru_cache
def get_settings() -> Settings:
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    return Settings(
        app_name="EduPath AI API",
        api_prefix="/api/v1",
        database_url=os.getenv("DATABASE_URL", "sqlite:///./edupath_ai.db"),
        cors_origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],
    )
