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
    db_url = os.getenv("DATABASE_URL", "sqlite:///./EDUPATH_ai.db")
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
    return Settings(
        app_name="EDUPATH API",
        api_prefix="/api/v1",
        database_url=db_url,
        cors_origins=["*"],
    )
