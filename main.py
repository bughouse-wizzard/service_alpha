from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Service Alpha", version="1.0.0")

# Configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
ZAKUPKI_BASE_URL = os.getenv("ZAKUPKI_BASE_URL", "https://zakupki.gov.ru")

# Import Celery app
try:
    from app.worker import celery_app, perform_search_task
    CELERY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Celery app: {e}")
    CELERY_AVAILABLE = False

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    version: str
    celery: str

class OrderRequest(BaseModel):
    item_id: str
    quantity: int = 1

class OrderResponse(BaseModel):
    order_id: str
    status: str
    item_id: str
    quantity: int
    message: Optional[str] = None

class SearchTaskRequest(BaseModel):
    object_name: str
    input_source: str = "manual"
    ktru_code: Optional[str] = None
    limit_contracts: Optional[int] = 10

class SearchTaskResponse(BaseModel):
    search_id: str
    task_id: str
    status: str
    message: str
    object_name: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        database="connected" if DATABASE_URL else "disconnected",
        redis="connected" if REDIS_URL else "disconnected",
        celery="connected" if CELERY_AVAILABLE else "disconnected",
        version="1.0.0"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Service Alpha",
        "version": "1.0.0",
        "description": "FastAPI service with PostgreSQL and Redis",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Order endpoint (example endpoint)
@app.post("/order", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    """Create a new order"""
    # This is a simplified example - in real implementation,
    # you would save to database, process with Celery, etc.
    
    # Generate a simple order ID
    import uuid
    order_id = str(uuid.uuid4())[:8]
    
    return OrderResponse(
        order_id=order_id,
        status="confirmed",
        item_id=order.item_id,
        quantity=order.quantity,
        message=f"Order {order_id} created successfully"
    )

# Example endpoint for testing external API
@app.get("/test-zakupki")
async def test_zakupki():
    """Test connection to Zakupki API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ZAKUPKI_BASE_URL, timeout=10.0)
            return {
                "status": "success",
                "zakupki_url": ZAKUPKI_BASE_URL,
                "response_status": response.status_code
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to Zakupki: {str(e)}")

# Search task endpoint
@app.post("/search", response_model=SearchTaskResponse)
async def create_search_task(search_request: SearchTaskRequest):
    """Create a new search task"""
    if not CELERY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Celery worker is not available. Please check if worker.py is properly configured."
        )
    
    # Generate search ID
    search_id = str(uuid.uuid4())
    
    # In a real implementation, you would save the search request to database here
    # For now, we'll just log it and trigger the task
    
    print(f"Creating search task: search_id={search_id}, object_name={search_request.object_name}")
    
    # Trigger the Celery task
    try:
        task = perform_search_task.delay(search_id)
        task_id = task.id
        
        print(f"Celery task triggered: task_id={task_id}")
        
        return SearchTaskResponse(
            search_id=search_id,
            task_id=task_id,
            status="pending",
            message="Search task created and queued for processing",
            object_name=search_request.object_name
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger search task: {str(e)}"
        )

# Task status endpoint
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a Celery task"""
    if not CELERY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Celery worker is not available"
        )
    
    try:
        task = celery_app.AsyncResult(task_id)
        
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None,
            "successful": task.successful() if task.ready() else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task status: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
