"""
Simple Celery worker configuration for Service Alpha (without database dependency).
"""
import os
import time
from celery import Celery
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
    "service_alpha_simple",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.worker_simple"]
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


@celery_app.task(bind=True, name="perform_search_task_simple")
def perform_search_task_simple(self, search_id: str) -> dict:
    """Perform search task (simplified version without database).
    
    Args:
        search_id: The search request ID
        
    Returns:
        dict: Task result with status and details
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} started for search {search_id}")
    
    try:
        # Simulate work
        total_iterations = 10
        for i in range(total_iterations):
            # Simulate work
            time.sleep(0.5)  # 500ms per iteration
            
            # Update progress periodically
            if i % 2 == 0:
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