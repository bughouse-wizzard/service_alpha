import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.models import Base

# Load environment variables
load_dotenv()

# Get database URL from environment, fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
SYNC_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# If DATABASE_URL is PostgreSQL async, create sync version for Celery
if "postgresql+asyncpg" in DATABASE_URL:
    SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# For synchronous operations (like in Celery tasks)
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in SYNC_DATABASE_URL else {},
)
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def init_db():
    """Initialize database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_db():
    """Get synchronous database session for Celery tasks."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()