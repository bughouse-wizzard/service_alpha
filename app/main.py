import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import redis
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from app.logging_config import setup_logging
from app.database import engine, get_db

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    db_url: str = "postgresql://postgres:postgres@db:5432/service_alpha"
    redis_url: str = "redis://redis:6379/0"
    log_level: str = "INFO"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "service_alpha"
    db_host: str = "db"
    db_port: str = "5432"
    redis_host: str = "redis"
    redis_port: str = "6379"
    deepseek_api_key: str = "your_deepseek_api_key_here"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: str = "8000"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"
    
    class Config:
        env_file = ".env"


settings = Settings()


# Redis setup
redis_client = redis.from_url(settings.redis_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting up FastAPI application")
    
    # Test database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
    
    # Test Redis connection
    try:
        redis_client.ping()
        logger.info("Redis connection successful")
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application")
    engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="Service Alpha API",
    description="FastAPI service with PostgreSQL, Redis, and Celery",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    timestamp: str


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Service Alpha API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    import datetime
    
    # Check database
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "unhealthy"
    
    # Check Redis
    redis_status = "healthy"
    try:
        redis_client.ping()
    except redis.ConnectionError:
        redis_status = "unhealthy"
    
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        redis=redis_status,
        timestamp=datetime.datetime.utcnow().isoformat()
    )


@app.get("/items/{item_id}", tags=["Items"])
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Example endpoint to read an item."""
    logger.info(f"Reading item with ID: {item_id}")
    
    # This is a placeholder - in a real app, you would query the database
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": "This is a sample item"
    }


@app.post("/items/", tags=["Items"])
async def create_item(item_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Example endpoint to create an item."""
    logger.info(f"Creating item with data: {item_data}")
    
    # This is a placeholder - in a real app, you would insert into the database
    return {
        "message": "Item created successfully",
        "item_id": 123,
        "data": item_data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host if hasattr(settings, 'app_host') else "0.0.0.0",
        port=int(settings.app_port) if hasattr(settings, 'app_port') else 8000,
        reload=True
    )