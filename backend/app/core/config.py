"""
CarePath AI Core Configuration Module
====================================
Uses Pydantic v2 BaseSettings to load, validate, and expose environment configuration
for database connections, JWT security, upload constraints, and CORS policies.
"""

from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API & Project Info
    PROJECT_NAME: str = "CarePath AI Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "carepath_admin"
    POSTGRES_PASSWORD: str = "secure_password_change_me"
    POSTGRES_DB: str = "carepath_db"
    DATABASE_URL: str = "postgresql+asyncpg://carepath_admin:secure_password_change_me@localhost:5432/carepath_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # JWT Authentication & Security
    SECRET_KEY: str = "default_development_secret_key_change_in_production_32bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://carepath.ai",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "png", "jpg", "jpeg", "dicom"]

    # PHI Security
    PHI_SALT: str = "default_phi_salt_key"

    # External AI Services (Sprint 2 Integration)
    VISION_SERVICE_URL: str = "http://localhost:8001/api/v1/vision"
    OCR_SERVICE_URL: str = "http://localhost:8002/api/v1/ocr"
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Global Singleton Settings Instance
settings = Settings()
