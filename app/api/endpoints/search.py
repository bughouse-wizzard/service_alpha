import uuid
import json
import time
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import redis

from app.db import get_db
from app.models.search import SearchRequest, SearchStatus
from app.core.config import settings
from app.workers.tasks import execute_search_task
from app.services.report_generator import ReportGenerator

# Create router
router = APIRouter()

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL)

# Pydantic models for request/response
from pydantic import BaseModel, Field, field_validator
from typing import Optional as Opt

class SearchCreateRequest(BaseModel):
    """Request model for creating a search"""
    input_source: str = Field(..., description="Input source for search")
    ktru_code: Opt[str] = Field(None, description="KTRU code for filtering")
    limit_contracts: int = Field(10, description="Maximum number of contracts to process")
    selected_contract_ids: Opt[List[str]] = Field(None, description="Specific contract IDs to process")
    nmc_value: Opt[float] = Field(None, description="NMC value threshold")
    search_query: Opt[str] = Field(None, description="Search query text")
    region_filter: Opt[str] = Field(None, description="Region filter")
    date_from: Opt[str] = Field(None, description="Start date (YYYY-MM-DD)")
    date_to: Opt[str] = Field(None, description="End date (YYYY-MM-DD)")
    price_min: Opt[float] = Field(None, description="Minimum price")
    price_max: Opt[float] = Field(None, description="Maximum price")
    technical_specification: Opt[str] = Field(None, description="Technical specification text for comparison")
    ai_model_version: Opt[str] = Field(None, description="AI model version to use")
    confidence_threshold: float = Field(0.7, description="Confidence threshold for AI")

    @field_validator('date_from', 'date_to')
    @classmethod
    def validate_date_format(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class SearchResponse(BaseModel):
    """Response model for search details"""
    id: uuid.UUID
    input_source: str
    ktru_code: Opt[str]
    status: str
    limit_contracts: int
    selected_contract_ids: Opt[List[str]]
    nmc_value: Opt[float]
    search_query: Opt[str]
    region_filter: Opt[str]
    date_from: Opt[str]
    date_to: Opt[str]
    price_min: Opt[float]
    price_max: Opt[float]
    technical_specification: Opt[str]
    total_contracts_found: int
    contracts_processed: int
    processing_started_at: Opt[str]
    processing_completed_at: Opt[str]
    error_message: Opt[str]
    retry_count: int
    ai_model_version: Opt[str]
    confidence_threshold: float
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

@router.get("/api/searches", response_model=List[SearchResponse])
async def get_searches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all searches (search history)
    
    Returns paginated list of search requests for history view
    """
    searches = db.query(SearchRequest).order_by(SearchRequest.created_at.desc()).offset(skip).limit(limit).all()
    return searches

@router.post("/api/search", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_search(
    search_request: SearchCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new search request
    
    Validates input, creates SearchRequest in DB, triggers Celery task, returns ID
    """
    # Create search request in database
    db_search = SearchRequest(
        **search_request.model_dump()
    )
    
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    
    # Trigger Celery task to execute the search
    task_result = execute_search_task.delay(db_search.id)
    
    # Store task ID in Redis for tracking
    redis_client.set(f"search_task:{db_search.id}", task_result.id)
    
    return db_search

@router.post("/api/search/{search_id}/stop", status_code=status.HTTP_200_OK)
async def stop_search(search_id: uuid.UUID):
    """
    Stop a running search by setting Redis stop signal
    """
    # Set stop signal in Redis
    redis_key = f"stop_signal:{search_id}"
    redis_client.set(redis_key, "1", ex=3600)  # Expire after 1 hour
    
    return {"message": f"Stop signal sent for search {search_id}", "search_id": str(search_id)}

@router.get("/api/search/{search_id}", response_model=SearchResponse)
async def get_search(
    search_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get search details by ID
    """
    search = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
    
    if not search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search with ID {search_id} not found"
        )
    
    return search

@router.get("/api/search/{search_id}/events")
async def stream_search_events(search_id: uuid.UUID):
    """
    Stream search progress updates via Server-Sent Events (SSE)
    
    Returns processed_count and logs as they become available
    """
    async def event_generator():
        # Create a new database session for the generator
        from app.db import SessionLocal
        db = SessionLocal()
        
        try:
            # Check if search exists
            search = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
            
            if not search:
                yield f"data: {json.dumps({'error': 'Search not found'})}\n\n"
                return
            
            # Initial status
            yield f"data: {json.dumps({'status': 'connected', 'search_id': str(search_id)})}\n\n"
            
            # Get current progress from Redis or database
            last_processed = search.contracts_processed
            
            while True:
                # Check for stop signal
                stop_signal = redis_client.get(f"stop_signal:{search_id}")
                if stop_signal:
                    yield f"data: {json.dumps({'status': 'stopped', 'message': 'Search stopped by user'})}\n\n"
                    break
                
                # Refresh search object from database
                db.refresh(search)
                
                if search.status == SearchStatus.COMPLETED:
                    yield f"data: {json.dumps({'status': 'completed', 'processed_count': search.contracts_processed, 'total': search.total_contracts_found})}\n\n"
                    break
                elif search.status == SearchStatus.FAILED:
                    yield f"data: {json.dumps({'status': 'failed', 'error': search.error_message})}\n\n"
                    break
                elif search.status == SearchStatus.CANCELLED:
                    yield f"data: {json.dumps({'status': 'cancelled', 'message': 'Search cancelled'})}\n\n"
                    break
                
                # Send progress update if changed
                if search.contracts_processed > last_processed:
                    yield f"data: {json.dumps({'status': 'processing', 'processed_count': search.contracts_processed, 'total': search.total_contracts_found})}\n\n"
                    last_processed = search.contracts_processed
                
                # Wait before next check
                time.sleep(1)
        finally:
            db.close()
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
    )


@router.get("/api/search/{search_id}/report")
async def get_search_report(
    search_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Generate and download NMCC calculation report for a search.
    
    Returns XLSX file with two sheets:
    1. Summary: NMCC calculation and input parameters
    2. Comparison Matrix: Specifications vs Contracts comparison
    """
    # Check if search exists
    search = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
    
    if not search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search with ID {search_id} not found"
        )
    
    # Check if search is completed
    if search.status != SearchStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search with ID {search_id} is not completed. Current status: {search.status.value}"
        )
    
    # Generate report
    try:
        report_generator = ReportGenerator(db)
        xlsx_file, filename = report_generator.generate_report(search_id)
        
        return StreamingResponse(
            xlsx_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache",
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )