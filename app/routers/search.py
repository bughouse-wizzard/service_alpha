import asyncio
import json
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
async def get_search_events(search_id: str):
    """
    Server-Sent Events (SSE) endpoint for search status updates.
    
    Yields status updates from Redis or DB polling.
    In this implementation, we simulate events with polling.
    """
    async def event_generator():
        """Generate SSE events for search status updates."""
        # In production, this would connect to Redis pub/sub or poll database
        # For simulation, we'll send a few status updates
        
        events = [
            {"event": "status", "data": {"status": "PROCESSING", "message": "Search started"}},
            {"event": "progress", "data": {"processed": 10, "total": 100, "percentage": 10}},
            {"event": "progress", "data": {"processed": 50, "total": 100, "percentage": 50}},
            {"event": "progress", "data": {"processed": 100, "total": 100, "percentage": 100}},
            {"event": "status", "data": {"status": "COMPLETED", "message": "Search completed successfully"}},
        ]
        
        for i, event_data in enumerate(events):
            # Format as SSE
            event = schemas.SearchEvent(
                event=event_data["event"],
                data=event_data["data"],
                id=str(i),
                retry=3000  # 3 seconds retry
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
            
            # Wait before sending next event
            await asyncio.sleep(1)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering for nginx
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