from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import search

app = FastAPI(
    title="Service Alpha API",
    description="Backend API for Service Alpha",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router)

from fastapi.staticfiles import StaticFiles

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Service Alpha API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)