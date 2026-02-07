import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DB_URL: str = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/service_alpha")
    DATABASE_URL: Optional[str] = None  # For compatibility with .env file
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # DeepSeek API
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_TEMPERATURE: float = 0.1
    DEEPSEEK_MAX_TOKENS: int = 4000
    
    # Application
    APP_NAME: str = "Service Alpha"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }


settings = Settings()

# Use DATABASE_URL from .env if provided, otherwise use DB_URL
if settings.DATABASE_URL:
    settings.DB_URL = settings.DATABASE_URL