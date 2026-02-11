import time
import uuid
from celery import Celery
from sqlalchemy.orm import Session

from app.database import SyncSessionLocal, get_sync_db
from app.models import SearchStatus, SearchRequest

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
def process_search_task(self, search_id: str):
    """
    Celery task to process a search request.
    
    This is a stub implementation that simulates search processing.
    In a real implementation, this would:
    1. Fetch search request from database
    2. Perform actual search logic (HTTP requests, parsing, etc.)
    3. Update search status and results
    4. Store contract results in database
    
    Args:
        search_id: String ID of the search request to process
    """
    
    # Get database session
    db: Session = next(get_sync_db())
    
    try:
        # Fetch search request
        search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
        
        if not search_request:
            self.update_state(state="FAILURE", meta={"error": f"Search request {search_id} not found"})
            return
        
        # Update status to PROCESSING
        search_request.status = SearchStatus.PROCESSING
        db.commit()
        
        # Simulate search processing
        total_items = 100
        for i in range(total_items):
            # Simulate work
            time.sleep(0.1)
            
            # Update progress
            progress = (i + 1) / total_items * 100
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": i + 1,
                    "total": total_items,
                    "percent": progress,
                    "status": f"Processing item {i + 1}/{total_items}"
                }
            )
        
        # Update search request with results
        search_request.status = SearchStatus.COMPLETED
        search_request.found_total = 50  # Simulated result count
        search_request.processed_count = total_items
        db.commit()
        
        return {
            "search_id": search_id,
            "status": "completed",
            "found_total": 50,
            "processed_count": total_items
        }
        
    except Exception as e:
        # Update status to FAILED on error
        try:
            search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
            if search_request:
                search_request.status = SearchStatus.FAILED
                db.commit()
        except:
            pass
        
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
    finally:
        db.close()


if __name__ == "__main__":
    celery_app.start()