import asyncio
import json
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models, schemas
from app.celery_app import process_search_task
from app.database import get_db
from app.models import SearchStatus

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=schemas.SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_search(
    search_data: schemas.SearchCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new search request.
    
    Accepts JSON payload, creates a SearchRequest record with status 'RUNNING',
    triggers a Celery task, and returns the search ID.
    """
    # Create search request with status RUNNING
    search_request = models.SearchRequest(
        input_source=search_data.input_source,
        object_name=search_data.object_name,
        ktru_code=search_data.ktru_code,
        nmc_value=search_data.nmc_value,
        limit_contracts=search_data.limit_contracts,
        status=SearchStatus.RUNNING,
        found_total=0,
        processed_count=0,
    )
    
    db.add(search_request)
    await db.commit()
    await db.refresh(search_request)
    
    # Trigger Celery task for search processing
    process_search_task.delay(str(search_request.id))
    
    return search_request


@router.get("/{search_id}", response_model=schemas.SearchResponse)
async def get_search(
    search_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get search request details by ID.
    """
    result = await db.execute(
        select(models.SearchRequest).where(models.SearchRequest.id == search_id)
    )
    search_request = result.scalar_one_or_none()
    
    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search request with ID {search_id} not found"
        )
    
    return search_request


@router.get("/{search_id}/results", response_model=List[schemas.ContractResultResponse])
async def get_search_results(
    search_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get contract results for a specific search request.
    """
    # First check if search exists
    result = await db.execute(
        select(models.SearchRequest).where(models.SearchRequest.id == search_id)
    )
    search_request = result.scalar_one_or_none()
    
    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search request with ID {search_id} not found"
        )
    
    # Get contract results
    result = await db.execute(
        select(models.ContractResult)
        .where(models.ContractResult.search_id == search_id)
        .order_by(models.ContractResult.reestr_number)
    )
    contract_results = result.scalars().all()
    
    return contract_results


@router.post("/{search_id}/stop", response_model=schemas.SearchResponse)
async def stop_search(
    search_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Stop a running search request by updating its status to 'STOPPED'.
    """
    result = await db.execute(
        select(models.SearchRequest).where(models.SearchRequest.id == search_id)
    )
    search_request = result.scalar_one_or_none()
    
    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search request with ID {search_id} not found"
        )
    
    # Update status to STOPPED
    search_request.status = SearchStatus.STOPPED
    await db.commit()
    await db.refresh(search_request)
    
    return search_request


@router.get("/{search_id}/events")
async def get_search_events(search_id: str, db: AsyncSession = Depends(get_db)):
    """
    Server-Sent Events (SSE) endpoint for search status updates.
    
    Uses Redis pub/sub for real-time event streaming.
    """
    # First, check if search exists
    search_request = await db.get(SearchRequest, search_id)
    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search request with ID {search_id} not found"
        )
    
    async def event_generator():
        """Generate SSE events from Redis subscription."""
        from app.services.redis_service import get_redis_service
        
        try:
            # Get Redis service
            redis_service = await get_redis_service()
            
            # Send initial status from database
            initial_event = schemas.SearchEvent(
                event="status",
                data={
                    "status": search_request.status.value,
                    "message": f"Search is {search_request.status.value.lower()}",
                    "search_id": search_id,
                    "processed_count": search_request.processed_count,
                    "found_total": search_request.found_total,
                    "nmc_value": str(search_request.nmc_value) if search_request.nmc_value else None
                },
                id="initial",
                retry=3000
            )
            
            # Send initial event
            lines = []
            if initial_event.id:
                lines.append(f"id: {initial_event.id}")
            if initial_event.event:
                lines.append(f"event: {initial_event.event}")
            if initial_event.retry:
                lines.append(f"retry: {initial_event.retry}")
            
            lines.append(f"data: {json.dumps(initial_event.data)}")
            yield "\n".join(lines) + "\n\n"
            
            # Subscribe to Redis channel for this search
            async for event_data in redis_service.subscribe_to_search(search_id):
                try:
                    # Format as SSE
                    event = schemas.SearchEvent(
                        event=event_data.get("event", "message"),
                        data=event_data.get("data", {}),
                        id=str(uuid.uuid4()),
                        retry=3000
                    )
                    
                    # Convert to SSE format
                    lines = []
                    if event.id:
                        lines.append(f"id: {event.id}")
                    if event.event:
                        lines.append(f"event: {event.event}")
                    if event.retry:
                        lines.append(f"retry: {event.retry}")
                    
                    lines.append(f"data: {json.dumps(event.data)}")
                    
                    yield "\n".join(lines) + "\n\n"
                    
                except Exception as e:
                    logger.error(f"Error formatting SSE event: {e}")
                    # Send error event
                    error_event = schemas.SearchEvent(
                        event="error",
                        data={"error": "Failed to format event"},
                        id=str(uuid.uuid4()),
                        retry=3000
                    )
                    
                    lines = [
                        f"id: {error_event.id}",
                        f"event: {error_event.event}",
                        f"retry: {error_event.retry}",
                        f"data: {json.dumps(error_event.data)}"
                    ]
                    yield "\n".join(lines) + "\n\n"
        
        except asyncio.CancelledError:
            logger.info(f"SSE connection cancelled for search {search_id}")
            raise
        
        except Exception as e:
            logger.error(f"Error in SSE event generator: {e}")
            
            # Send final error event
            error_event = schemas.SearchEvent(
                event="error",
                data={"error": f"Connection error: {str(e)}"},
                id="final_error",
                retry=None  # No retry on fatal error
            )
            
            lines = [
                f"id: {error_event.id}",
                f"event: {error_event.event}",
                f"data: {json.dumps(error_event.data)}"
            ]
            yield "\n".join(lines) + "\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
    )


@router.get("/{search_id}/detail", response_model=schemas.SearchDetailResponse)
async def get_search_detail(
    search_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get search request details with contract results.
    """
    result = await db.execute(
        select(models.SearchRequest)
        .where(models.SearchRequest.id == search_id)
        .options(selectinload(models.SearchRequest.contract_results))
    )
    search_request = result.scalar_one_or_none()
    
    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Search request with ID {search_id} not found"
        )
    
    return search_request