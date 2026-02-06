import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/service_alpha"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # DeepSeek API
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # Application
    APP_NAME: str = "Service Alpha"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()