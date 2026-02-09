import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment or use SQLite for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
TEST_DATABASE_URL = os.getenv("DATABASE_TEST_URL", "sqlite:///./test.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    poolclass=StaticPool if DATABASE_URL.startswith("sqlite") else None
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()