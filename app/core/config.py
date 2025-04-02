import secrets
from typing import Any, Literal

from pydantic import (
    PostgresDsn,
    computed_field,
    field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    PORT: int = 8000  # Add default value 8000

    @field_validator("PORT", mode="before")
    def get_port(cls, v: Any | None) -> int:
        """Get PORT from env or use default 8000"""
        if isinstance(v, str):
            return int(v)
        return v or 8000

    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14
    RESET_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    ENVIRONMENT: Literal["local", "staging", "production", "test"] = "local"
    BACKEND_CORS_ORIGINS: str | list[str] = "http://localhost:8000"
    PROJECT_NAME: str = "FastAPI"

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_DB_TEST: str = "stockbot_test"

    # Email settings
    SMTP_SERVER: str = "ap-northeast-1"
    SMTP_PORT: int = 587
    SMTP_TLS: bool = True
    SMTP_ACCESS_KEY: str = ""
    SMTP_SECRET_KEY: str = ""
    SMTP_SENDER: str = "noreply@yourdomain.com"
    FRONT_END_URL: str = "https://dev.stock.picontechnology.com"

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # edinet key

    EDINET_API_KEY: str

    # s3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET: str
    AWS_REGION: str
    BUCKET: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
