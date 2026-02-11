"""
Celery worker configuration for Service Alpha.
"""
import os
import time
import asyncio
import json
import tempfile
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy import create_engine, select, update
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
    try:
        from app.models import SearchRequest, SearchStatus
        # Query the search request to check if status is STOPPED
        search_request = db_session.get(SearchRequest, search_id)
        if search_request and search_request.status == SearchStatus.STOPPED:
            logger.info(f"Stop signal detected for search {search_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking stop signal for search {search_id}: {e}")
        return False


def run_async(coro):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


async def download_contract_document(contract_url: str) -> Optional[bytes]:
    """Download contract document from URL.
    
    Args:
        contract_url: URL to contract document
    
    Returns:
        Document content as bytes, or None if download fails
    """
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(contract_url)
            response.raise_for_status()
            return response.content
    except Exception as e:
        logger.error(f"Failed to download document from {contract_url}: {e}")
        return None


def publish_progress(search_id: str, progress: float, message: str = ""):
    """Publish progress to Redis/SSE channel.
    
    Args:
        search_id: Search request ID
        progress: Progress percentage (0.0 to 1.0)
        message: Optional progress message
    """
    try:
        import redis
        redis_client = redis.from_url(REDIS_URL)
        progress_data = {
            "search_id": search_id,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        redis_client.publish(f"search_progress:{search_id}", json.dumps(progress_data))
        logger.debug(f"Published progress for search {search_id}: {progress:.1%} - {message}")
    except Exception as e:
        logger.warning(f"Failed to publish progress to Redis: {e}")


@celery_app.task(bind=True, name="perform_search_task")
def perform_search_task(self, search_id: str) -> dict:
    """Perform search task: Scraper -> AI -> DB integration.
    
    Steps:
    1. Get search request from DB
    2. Call Scraper to get contract list
    3. Loop through contracts (checking stop signal)
    4. Parse details & download docs
    5. Call doc_extractor
    6. Call extract_specs_from_contract
    7. Call compare_specs against user's TZ
    8. Save ContractResult and SpecComparisonRow to DB
    9. Update processed_count in SearchRequest
    10. Publish progress to Redis/SSE channel
    
    Args:
        search_id: The search request ID
    
    Returns:
        dict: Task result with status and details
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} started for search {search_id}")
    
    db_session = None
    try:
        # Get database session
        db_session = get_db_session()
        
        # Import models and services
        from app.models import SearchRequest, ContractResult, SpecComparisonRow, SearchStatus, MatchType, MatchStatus
        from app.services.scraper.searcher import ZakupkiSearcher, SearchParams
        from app.services.docs.extractor import DocumentExtractor
        from app.services.ai.prompts import extract_specs_from_contract, compare_specs, extract_specs_from_tz
        
        # 1. Get search request from DB
        search_request = db_session.get(SearchRequest, search_id)
        if not search_request:
            raise ValueError(f"Search request {search_id} not found")
        
        # Update status to running
        search_request.status = SearchStatus.RUNNING
        db_session.commit()
        
        publish_progress(search_id, 0.0, "Starting search...")
        
        # 2. Call Scraper to get contract list
        logger.info(f"Searching contracts for: {search_request.object_name}")
        publish_progress(search_id, 0.1, "Searching for contracts...")
        
        # Prepare search parameters
        search_params = SearchParams(
            ktru=search_request.ktru_code,
            limit_contracts=search_request.limit_contracts
        )
        
        # Run async scraper in sync context
        async def search_contracts():
            async with ZakupkiSearcher() as searcher:
                return await searcher.search(search_params)
        
        search_result = run_async(search_contracts())
        
        if not search_result.contracts:
            logger.warning(f"No contracts found for search {search_id}")
            search_request.status = SearchStatus.COMPLETED
            search_request.found_total = 0
            db_session.commit()
            publish_progress(search_id, 1.0, "No contracts found")
            return {
                "status": "completed",
                "message": "No contracts found",
                "search_id": search_id,
                "found_total": 0,
                "processed_count": 0
            }
        
        # Update found total
        search_request.found_total = search_result.found_total
        db_session.commit()
        
        logger.info(f"Found {len(search_result.contracts)} contracts (total: {search_result.found_total})")
        publish_progress(search_id, 0.2, f"Found {len(search_result.contracts)} contracts")
        
        # Extract specs from TZ (technical requirements)
        # For now, we'll use a mock TZ text - in production this would come from search_request.input_source
        tz_text = search_request.input_source or f"Технические требования для {search_request.object_name}"
        target_specs = extract_specs_from_tz(tz_text)
        
        # Initialize document extractor
        doc_extractor = DocumentExtractor(ocr_fallback=False)
        
        # 3. Loop through contracts
        processed_count = 0
        total_contracts = len(search_result.contracts)
        
        for i, contract in enumerate(search_result.contracts):
            # Check stop signal
            if check_stop_signal(search_id, db_session):
                logger.info(f"Task {task_id} stopped by signal while processing contract {i+1}/{total_contracts}")
                search_request.status = SearchStatus.STOPPED
                db_session.commit()
                publish_progress(search_id, i/total_contracts, "Search stopped by user")
                return {
                    "status": "stopped",
                    "message": "Search stopped by user",
                    "search_id": search_id,
                    "processed_count": processed_count,
                    "progress": i/total_contracts
                }
            
            contract_progress = 0.2 + (i / total_contracts) * 0.7
            publish_progress(search_id, contract_progress, f"Processing contract {i+1}/{total_contracts}: {contract.reestr_number}")
            
            try:
                logger.info(f"Processing contract {i+1}/{total_contracts}: {contract.reestr_number}")
                
                # 4. Parse details & download docs
                contract_url = contract.link
                document_content = None
                extracted_text = ""
                
                if contract_url:
                    # Download document
                    document_content = run_async(download_contract_document(contract_url))
                    
                    # 5. Call doc_extractor if document downloaded
                    if document_content:
                        # Save to temporary file for extraction
                        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                            temp_file.write(document_content)
                            temp_path = temp_file.name
                        
                        try:
                            extracted_text = doc_extractor.extract_text(temp_path)
                        finally:
                            # Clean up temp file
                            os.unlink(temp_path)
                
                # 6. Call extract_specs_from_contract
                contract_specs_result = extract_specs_from_contract(extracted_text)
                contract_specs = contract_specs_result.get("specs", [])
                manufacturer = contract_specs_result.get("manufacturer")
                
                # 7. Call compare_specs against user's TZ
                comparison_result = compare_specs(target_specs, contract_specs)
                score = comparison_result.get("score", 0)
                match_type_str = comparison_result.get("match_type", "no_match")
                diff_log = comparison_result.get("diff_log", [])
                
                # Convert match_type string to MatchType enum
                match_type = MatchType.NO_MATCH
                if match_type_str == "exact":
                    match_type = MatchType.EXACT
                elif match_type_str == "partial":
                    match_type = MatchType.PARTIAL
                elif match_type_str == "similar":
                    match_type = MatchType.SIMILAR
                
                # 8. Save ContractResult and SpecComparisonRow to DB
                contract_result = ContractResult(
                    search_id=search_id,
                    reestr_number=contract.reestr_number,
                    contract_url=contract_url,
                    sign_date=contract.date,
                    unit_price=Decimal(str(contract.price)) if contract.price else None,
                    match_type=match_type,
                    ai_score=score,
                    manufacturer_target=None,  # Would come from TZ in production
                    manufacturer_found=manufacturer,
                    raw_data_json={
                        "contract_info": {
                            "reestr_number": contract.reestr_number,
                            "date": contract.date.isoformat() if contract.date else None,
                            "price": contract.price,
                            "link": contract_url
                        },
                        "extracted_text_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                        "specs_found": contract_specs,
                        "comparison_result": comparison_result
                    }
                )
                
                db_session.add(contract_result)
                db_session.flush()  # Get the ID for foreign key
                
                # Save spec comparison rows
                for diff_item in diff_log:
                    spec_name = diff_item.get("spec_name", "")
                    status_str = diff_item.get("status", "")
                    
                    # Convert status string to MatchStatus enum
                    match_status = MatchStatus.NOT_APPLICABLE
                    if status_str == "match":
                        match_status = MatchStatus.MATCH
                    elif status_str == "mismatch":
                        match_status = MatchStatus.PARTIAL_MATCH
                    elif status_str == "missing":
                        match_status = MatchStatus.NO_MATCH
                    
                    spec_row = SpecComparisonRow(
                        contract_result_id=contract_result.id,
                        name=spec_name,
                        target_value=str(diff_item.get("target", "")),
                        actual_value=str(diff_item.get("actual", "")),
                        match_status=match_status,
                        weight=diff_item.get("weight", 1)
                    )
                    db_session.add(spec_row)
                
                processed_count += 1
                
                # Update processed count periodically
                if (i + 1) % 5 == 0 or (i + 1) == total_contracts:
                    search_request.processed_count = processed_count
                    db_session.commit()
                    publish_progress(search_id, contract_progress + 0.05, f"Processed {i+1}/{total_contracts} contracts")
                
            except Exception as contract_error:
                logger.error(f"Error processing contract {contract.reestr_number}: {contract_error}")
                # Continue with next contract even if this one fails
                continue
        
        # 9. Update SearchRequest with final status
        search_request.status = SearchStatus.COMPLETED
        search_request.processed_count = processed_count
        db_session.commit()
        
        publish_progress(search_id, 1.0, f"Search completed. Processed {processed_count}/{total_contracts} contracts")
        
        logger.info(f"Task {task_id} completed successfully for search {search_id}. Processed {processed_count} contracts.")
        
        return {
            "status": "completed",
            "message": f"Search completed successfully. Processed {processed_count} contracts.",
            "search_id": search_id,
            "found_total": search_result.found_total,
            "processed_count": processed_count,
            "progress": 1.0
        }
        
    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {e}")
        
        # Update search request status to failed
        if db_session:
            try:
                from app.models import SearchRequest, SearchStatus
                search_request = db_session.get(SearchRequest, search_id)
                if search_request:
                    search_request.status = SearchStatus.FAILED
                    db_session.commit()
            except Exception as db_error:
                logger.error(f"Failed to update search request status: {db_error}")
        
        publish_progress(search_id, 0.0, f"Search failed: {str(e)}")
        
        return {
            "status": "error",
            "message": str(e),
            "search_id": search_id
        }
    finally:
        if db_session:
            db_session.close()


if __name__ == "__main__":
    # For testing the worker directly
    celery_app.start()