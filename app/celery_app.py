import time
import uuid
import logging
from celery import Celery
from sqlalchemy.orm import Session

from app.database import SyncSessionLocal, get_sync_db
from app.models import SearchStatus, SearchRequest
from app.services.orchestrator import OrchestrationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery application
celery_app = Celery(
    "service_alpha",
    broker="redis://localhost:6379/0",  # Default Redis URL
    backend="redis://localhost:6379/0",
    include=["app.celery_app"]  # Include this module
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
    worker_max_tasks_per_child=100,
)


@celery_app.task(bind=True, name="process_search_task")
def process_search_task(self, search_id: str, search_params: dict = None, tz_text: str = ""):
    """
    Celery task to process a search request using the orchestrator.
    
    This implementation uses the OrchestrationService to perform:
    1. Search for contracts using scraper
    2. Parse contract details
    3. Extract document content
    4. Process with AI for specification extraction and comparison
    5. Normalize and match specifications
    6. Calculate NMC values
    7. Store results in database
    
    Args:
        search_id: String ID of the search request to process
        search_params: Search parameters (optional, will be fetched from DB if not provided)
        tz_text: Technical specification text (optional)
    """
    
    # Get database session
    db: Session = next(get_sync_db())
    
    try:
        # Fetch search request
        search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
        
        if not search_request:
            self.update_state(state="FAILURE", meta={"error": f"Search request {search_id} not found"})
            return
        
        logger.info(f"Starting search task for {search_id}")
        
        # Update status to PROCESSING
        search_request.status = SearchStatus.PROCESSING
        db.commit()
        
        # Create orchestrator
        orchestrator = OrchestrationService(search_id, db)
        
        # If search_params not provided, extract from search_request
        if not search_params:
            search_params = {
                "law_type": "44-FZ",  # Default
                "region": None,
                "date_from": None,
                "date_to": None,
                "ktru_code": search_request.ktru_code,
                "limit_contracts": search_request.limit_contracts or 30
            }
        
        # Execute search using orchestrator
        result = orchestrator.execute_search(search_params, tz_text)
        
        # Update task state based on result
        if result["status"] == "completed":
            self.update_state(
                state="SUCCESS",
                meta={
                    "search_id": search_id,
                    "status": "completed",
                    "processed_count": result["processed_count"],
                    "found_total": result["found_total"],
                    "nmc_value": result.get("nmc_value")
                }
            )
            
            logger.info(f"Search task {search_id} completed successfully")
            return result
            
        elif result["status"] == "stopped":
            self.update_state(
                state="SUCCESS",  # Task completed successfully (was stopped by user)
                meta={
                    "search_id": search_id,
                    "status": "stopped",
                    "processed_count": result["processed_count"],
                    "found_total": result["found_total"]
                }
            )
            
            logger.info(f"Search task {search_id} stopped by user")
            return result
            
        else:
            raise RuntimeError(f"Unexpected status: {result['status']}")
        
    except Exception as e:
        logger.error(f"Search task {search_id} failed with error: {e}")
        
        # Update status to FAILED on error
        try:
            search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
            if search_request:
                search_request.status = SearchStatus.FAILED
                db.commit()
        except Exception as inner_e:
            logger.error(f"Failed to update search status after error: {inner_e}")
        
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
        
    finally:
        db.close()


if __name__ == "__main__":
    celery_app.start()