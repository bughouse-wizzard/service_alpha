from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Service Alpha", version="1.0.0")

# Configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
ZAKUPKI_BASE_URL = os.getenv("ZAKUPKI_BASE_URL", "https://zakupki.gov.ru")

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    version: str

class OrderRequest(BaseModel):
    item_id: str
    quantity: int = 1

class OrderResponse(BaseModel):
    order_id: str
    status: str
    item_id: str
    quantity: int
    message: Optional[str] = None

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        database="connected" if DATABASE_URL else "disconnected",
        redis="connected" if REDIS_URL else "disconnected",
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
