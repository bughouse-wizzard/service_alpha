import uuid
import time
import redis
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.core.celery_app import celery_app
from app.core.config import settings
from app.models.search import SearchRequest, SearchStatus


def get_db_session():
    """Create a database session"""
    engine = create_engine(settings.DB_URL)
    return Session(engine)


def get_redis_client():
    """Create a Redis client"""
    return redis.Redis.from_url(settings.REDIS_URL)


def _execute_search_task_logic(task_self, search_id: uuid.UUID):
    """
    Core logic for execute_search_task, separated for testing.
    
    Args:
        task_self: The Celery task instance (for update_state calls)
        search_id: UUID of the search request
    """
    redis_client = get_redis_client()
    stop_signal_key = f"stop_signal:{search_id}"
    
    try:
        # Get database session
        db = get_db_session()
        
        # Fetch search request from database
        search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
        
        if not search_request:
            task_self.update_state(state='FAILURE', meta={'error': f'Search request {search_id} not found'})
            return {'status': 'error', 'message': f'Search request {search_id} not found'}
        
        # Update status to RUNNING
        search_request.status = SearchStatus.PROCESSING
        db.commit()
        
        # Simulate work with periodic stop signal checks
        total_work_seconds = 5  # 5 seconds of mock work
        check_interval = 0.5    # Check stop signal every 0.5 seconds
        iterations = int(total_work_seconds / check_interval)
        
        for i in range(iterations):
            # Check for stop signal
            if redis_client.exists(stop_signal_key):
                # Stop signal detected - update status to CANCELLED
                search_request.status = SearchStatus.CANCELLED
                db.commit()
                db.close()
                
                # Clear the stop signal
                redis_client.delete(stop_signal_key)
                
                return {
                    'status': 'cancelled',
                    'message': f'Search {search_id} cancelled by stop signal',
                    'progress': i / iterations
                }
            
            # Simulate work
            time.sleep(check_interval)
            
            # Update progress
            progress = (i + 1) / iterations
            task_self.update_state(
                state='PROGRESS',
                meta={'current': i + 1, 'total': iterations, 'progress': progress}
            )
        
        # Work completed successfully
        search_request.status = SearchStatus.COMPLETED
        db.commit()
        db.close()
        
        return {
            'status': 'completed',
            'message': f'Search {search_id} completed successfully',
            'search_id': str(search_id)
        }
        
    except SQLAlchemyError as e:
        # Database error
        task_self.update_state(state='FAILURE', meta={'error': str(e)})
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
        
    except Exception as e:
        # General error
        task_self.update_state(state='FAILURE', meta={'error': str(e)})
        return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}


@celery_app.task
def example_task(message: str):
    """Example Celery task"""
    return f"Task completed: {message}"


@celery_app.task(bind=True)
def execute_search_task(self, search_id: uuid.UUID):
    """
    Execute search task with state management and stop signal support.
    
    Args:
        search_id: UUID of the search request
    """
    return _execute_search_task_logic(self, search_id)