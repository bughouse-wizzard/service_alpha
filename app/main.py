from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, get_db
from app.routers import search


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for FastAPI app."""
    # Initialize database on startup
    init_db()
    print("Database initialized")
    yield
    # Cleanup on shutdown
    print("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title="Service Alpha API",
    description="REST API for contract search and analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Service Alpha API",
        "version": "1.0.0",
        "description": "REST API for contract search and analysis",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "search": "/api/search",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "Service Alpha API",
        "database": "connected",  # Simplified - in production, check actual connection
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)