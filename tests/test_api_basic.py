import pytest
import asyncio
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager

from app.main import app
from app.database import get_db
from app.models import Base


# Test database URL - use file-based SQLite for tests to maintain connection
TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"


@pytest.fixture(scope="function")
def test_client():
    """Create a test client with overridden database dependency."""
    # Import here to avoid circular imports
    import app.main
    from app.database import get_db
    
    # Create async engine for testing
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    
    # Create all tables
    import asyncio
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(create_tables())
    
    # Create session factory
    TestingSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session
    
    # Override the get_db dependency
    app.main.app.dependency_overrides[get_db] = override_get_db
    
    # Mock the Celery task to avoid Redis connection
    # Patch at the source module where it's defined
    with patch('app.celery_app.process_search_task') as mock_celery_task:
        mock_celery_task.delay = MagicMock()
        # Also need to update the reference in the router module
        import app.routers.search
        app.routers.search.process_search_task = mock_celery_task
        with TestClient(app.main.app) as client:
            yield client
    
    # Cleanup
    app.main.app.dependency_overrides.clear()
    
    # Drop tables and clean up
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
    asyncio.run(drop_tables())
    
    # Remove test database file
    import os
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_create_search(test_client):
    """Test creating a search request."""
    search_data = {
        "input_source": "test_source",
        "object_name": "Test Object",
        "ktru_code": "123456",
        "nmc_value": 1000.50,
        "limit_contracts": 10
    }
    
    response = test_client.post("/api/search", json=search_data)
    
    assert response.status_code == 201
    data = response.json()
    
    # Check response structure
    assert "id" in data
    assert data["input_source"] == "test_source"
    assert data["object_name"] == "Test Object"
    assert data["ktru_code"] == "123456"
    assert data["nmc_value"] == "1000.50"  # Decimal is serialized as string
    assert data["limit_contracts"] == 10
    assert data["status"] == "running"  # Should be RUNNING status
    assert data["found_total"] == 0
    assert data["processed_count"] == 0
    assert "created_at" in data
    
    return data["id"]  # Return search ID for other tests


def test_get_search(test_client):
    """Test getting a search request by ID."""
    # First create a search
    search_data = {
        "input_source": "test_source",
        "object_name": "Test Object",
        "ktru_code": "123456"
    }
    
    create_response = test_client.post("/api/search", json=search_data)
    print(f"Create response status: {create_response.status_code}")
    print(f"Create response: {create_response.json()}")
    assert create_response.status_code == 201
    search_id = create_response.json()["id"]
    print(f"Search ID: {search_id}")
    
    # Now get the search
    response = test_client.get(f"/api/search/{search_id}")
    print(f"Get response status: {response.status_code}")
    print(f"Get response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["id"] == search_id
    assert data["input_source"] == "test_source"
    assert data["object_name"] == "Test Object"
    assert data["ktru_code"] == "123456"
    assert data["status"] == "running"


def test_get_nonexistent_search(test_client):
    """Test getting a non-existent search request."""
    response = test_client.get("/api/search/00000000-0000-0000-0000-000000000000")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_search_results_empty(test_client):
    """Test getting results for a search with no results."""
    # Create a search
    search_data = {
        "input_source": "test_source",
        "object_name": "Test Object"
    }
    
    create_response = test_client.post("/api/search", json=search_data)
    search_id = create_response.json()["id"]
    
    # Get results (should be empty list)
    response = test_client.get(f"/api/search/{search_id}/results")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 0


def test_stop_search(test_client):
    """Test stopping a search request."""
    # Create a search
    search_data = {
        "input_source": "test_source",
        "object_name": "Test Object"
    }
    
    create_response = test_client.post("/api/search", json=search_data)
    search_id = create_response.json()["id"]
    
    # Stop the search
    response = test_client.post(f"/api/search/{search_id}/stop")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check status was updated to STOPPED
    assert data["status"] == "stopped"
    
    # Verify by getting the search again
    get_response = test_client.get(f"/api/search/{search_id}")
    assert get_response.json()["status"] == "stopped"


def test_stop_nonexistent_search(test_client):
    """Test stopping a non-existent search request."""
    response = test_client.post("/api/search/00000000-0000-0000-0000-000000000000/stop")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_search_detail(test_client):
    """Test getting search details with relationships."""
    # Create a search
    search_data = {
        "input_source": "test_source",
        "object_name": "Test Object"
    }
    
    create_response = test_client.post("/api/search", json=search_data)
    search_id = create_response.json()["id"]
    
    # Get search detail
    response = test_client.get(f"/api/search/{search_id}/detail")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert data["id"] == search_id
    assert "contract_results" in data
    assert isinstance(data["contract_results"], list)


def test_root_endpoint(test_client):
    """Test the root endpoint."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "service" in data
    assert "version" in data
    assert "description" in data
    assert "endpoints" in data


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "service" in data
    assert "database" in data