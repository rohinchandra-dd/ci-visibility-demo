import os
from functools import lru_cache


class Settings:
    app_name: str = "Pulse Community"
    secret_key: str = os.getenv("PULSE_SECRET_KEY", "pulse-demo-secret-change-in-prod")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pulse.db",
    )
    cors_origins: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    ).split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()
