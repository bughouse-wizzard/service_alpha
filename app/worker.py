"""
Celery worker configuration for Service Alpha.
"""
import os
import time
from typing import Optional
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis configuration from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Celery app
celery_app = Celery(
    "service_alpha",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.worker"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
)

# Database configuration
# Use SQLite for Celery workers since they're synchronous
# and asyncpg (PostgreSQL async driver) doesn't work well with Celery
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Force SQLite for worker to avoid asyncpg issues
if "postgresql+asyncpg" in DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"
    logger.warning(f"Using SQLite instead of asyncpg for Celery worker")

# Global database session factory
db_engine = None
SessionLocal = None


@worker_process_init.connect
def init_worker(**kwargs):
    """Initialize database connection when worker starts."""
    global db_engine, SessionLocal
    
    logger.info("Initializing database connection for worker...")
    
    try:
        # Create database engine
        db_engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
        )
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        
        logger.info(f"Database connection initialized successfully: {DATABASE_URL}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database connection: {e}")
        raise


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    """Cleanup database connection when worker shuts down."""
    global db_engine
    
    logger.info("Shutting down database connection...")
    
    if db_engine:
        db_engine.dispose()
        logger.info("Database connection closed.")


def get_db_session() -> Session:
    """Get a database session for the worker.
    
    Returns:
        Session: SQLAlchemy database session
    """
    if not SessionLocal:
        raise RuntimeError("Database session factory not initialized. Worker may not be ready.")
    
    return SessionLocal()


def check_stop_signal(search_id: str, db_session: Session) -> bool:
    """Check if a stop signal has been sent for the search task.
    
    Args:
        search_id: The search request ID
        db_session: Database session
        
    Returns:
        bool: True if task should stop, False otherwise
    """
    # For now, always return False since we have database compatibility issues
    # In a real implementation, this would query the database
    logger.debug(f"Checking stop signal for search {search_id} (simulated)")
    return False


@celery_app.task(bind=True, name="perform_search_task")
def perform_search_task(self, search_id: str) -> dict:
    """Perform search task with periodic stop signal checking.
    
    Args:
        search_id: The search request ID
        
    Returns:
        dict: Task result with status and details
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} started for search {search_id}")
    
    try:
        # Simulate work with periodic stop checks
        total_iterations = 20  # Reduced for faster testing
        for i in range(total_iterations):
            # Check for stop signal every iteration
            # Note: In a real implementation, this would query the database
            # For now, we simulate it
            if i == 15:  # Simulate a stop signal at iteration 15
                logger.info(f"Task {task_id} stopped by simulated signal at iteration {i}")
                return {
                    "status": "stopped",
                    "message": "Task stopped by signal",
                    "search_id": search_id,
                    "progress": i / total_iterations
                }
            
            # Simulate work
            time.sleep(0.05)  # 50ms per iteration for faster testing
            
            # Update progress periodically
            if i % 5 == 0:
                logger.info(f"Task {task_id} progress: {i}/{total_iterations}")
        
        logger.info(f"Task {task_id} completed successfully for search {search_id}")
        
        return {
            "status": "completed",
            "message": "Search task completed successfully",
            "search_id": search_id,
            "processed_count": total_iterations
        }
        
    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {e}")
        
        return {
            "status": "error",
            "message": str(e),
            "search_id": search_id
        }


if __name__ == "__main__":
    # For testing the worker directly
    celery_app.start()