from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

# For testing, using SQLite. In production, use PostgreSQL
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()