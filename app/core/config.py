"""Application Settings and Environment Configuration."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "CarePath AI Platform"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # API Keys
    GEMINI_API_KEY: str = ""

    # Paths
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    UPLOADS_DIRECTORY: str = "./data/uploads"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Ensure required data directories exist
os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(settings.UPLOADS_DIRECTORY, exist_ok=True)
