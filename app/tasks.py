import logging
import time
from celery import Celery
from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"
    
    class Config:
        env_file = ".env"


celery_settings = CelerySettings()

# Create Celery app
celery_app = Celery(
    "service_alpha",
    broker=celery_settings.celery_broker_url,
    backend=celery_settings.celery_result_backend,
    include=["app.tasks"]
)

# Configure Celery
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
)

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_data_task")
def process_data_task(self, data: dict):
    """Example task to process data asynchronously."""
    task_id = self.request.id
    logger.info(f"Starting task {task_id} with data: {data}")
    
    try:
        # Simulate processing
        time.sleep(2)
        
        # Process data (example)
        result = {
            "task_id": task_id,
            "processed": True,
            "input_data": data,
            "output": f"Processed: {data.get('value', 'unknown')}",
            "timestamp": time.time()
        }
        
        logger.info(f"Task {task_id} completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        raise


@celery_app.task(bind=True, name="parse_document_task")
def parse_document_task(self, document_url: str, parser_type: str = "default"):
    """Task to parse documents - useful for debugging parser runs."""
    task_id = self.request.id
    logger.info(f"Starting document parsing task {task_id}: {document_url} ({parser_type})")
    
    try:
        # Log to parser-specific logger
        parser_logger = logging.getLogger("parser")
        parser_logger.info(f"Parser run started - Task: {task_id}, URL: {document_url}, Type: {parser_type}")
        
        # Simulate parsing
        time.sleep(3)
        
        # Example parsing logic
        result = {
            "task_id": task_id,
            "document_url": document_url,
            "parser_type": parser_type,
            "status": "success",
            "extracted_data": {
                "title": f"Document from {document_url}",
                "content_length": 1500,
                "entities_found": ["entity1", "entity2", "entity3"],
                "metadata": {"source": document_url, "parsed_at": time.time()}
            },
            "timestamp": time.time()
        }
        
        parser_logger.info(f"Parser run completed - Task: {task_id}, Results: {len(result['extracted_data']['entities_found'])} entities found")
        logger.info(f"Document parsing task {task_id} completed")
        
        return result
        
    except Exception as e:
        parser_logger.error(f"Parser run failed - Task: {task_id}, Error: {e}")
        logger.error(f"Document parsing task {task_id} failed: {e}")
        raise


@celery_app.task(bind=True, name="health_check_task")
def health_check_task(self):
    """Periodic health check task."""
    task_id = self.request.id
    logger.debug(f"Health check task {task_id} running")
    
    return {
        "task_id": task_id,
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "celery": "running",
            "redis": "connected"
        }
    }


# Periodic tasks configuration
celery_app.conf.beat_schedule = {
    "health-check-every-5-minutes": {
        "task": "app.tasks.health_check_task",
        "schedule": 300.0,  # 5 minutes
    },
}