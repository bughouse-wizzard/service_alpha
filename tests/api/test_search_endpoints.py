import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.db import get_db
from app.models.search import SearchRequest, SearchStatus

# Mock database session
mock_db = Mock()

# Create a real SearchRequest instance for testing
def create_test_search_request():
    search = SearchRequest()
    search.id = uuid.uuid4()
    search.input_source = "test_source"
    search.ktru_code = "123456"
    search.status = SearchStatus.PENDING
    search.limit_contracts = 5
    search.selected_contract_ids = None
    search.nmc_value = None
    search.search_query = "test query"
    search.region_filter = "Moscow"
    search.date_from = "2024-01-01"
    search.date_to = "2024-12-31"
    search.price_min = 1000.0
    search.price_max = 50000.0
    search.total_contracts_found = 0
    search.contracts_processed = 0
    search.processing_started_at = None
    search.processing_completed_at = None
    search.error_message = None
    search.retry_count = 0
    search.ai_model_version = None
    search.confidence_threshold = 0.8
    search.created_at = datetime.now()
    search.updated_at = datetime.now()
    return search

mock_search_request = create_test_search_request()

def mock_get_db():
    yield mock_db

app.dependency_overrides[get_db] = mock_get_db

client = TestClient(app)

def test_create_search():
    """Test creating a new search request"""
    # Mock the database operations
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    # Create a new mock for the search request that will be returned
    new_search = Mock(spec=SearchRequest)
    new_search.id = uuid.uuid4()
    new_search.input_source = "test_source"
    new_search.ktru_code = "123456"
    new_search.status = SearchStatus.PENDING.value
    new_search.limit_contracts = 5
    new_search.selected_contract_ids = None
    new_search.nmc_value = None
    new_search.search_query = "test query"
    new_search.region_filter = "Moscow"
    new_search.date_from = "2024-01-01"
    new_search.date_to = "2024-12-31"
    new_search.price_min = 1000.0
    new_search.price_max = 50000.0
    new_search.total_contracts_found = 0
    new_search.contracts_processed = 0
    new_search.processing_started_at = None
    new_search.processing_completed_at = None
    new_search.error_message = None
    new_search.retry_count = 0
    new_search.ai_model_version = None
    new_search.confidence_threshold = 0.8
    new_search.created_at = "2024-01-01T00:00:00"
    new_search.updated_at = "2024-01-01T00:00:00"
    
    # Mock refresh to set the search object
    def mock_refresh(obj):
        # Simulate setting attributes
        for attr, value in new_search.__dict__.items():
            if not attr.startswith('_'):
                setattr(obj, attr, value)
    
    mock_db.refresh.side_effect = mock_refresh
    
    search_data = {
        "input_source": "test_source",
        "ktru_code": "123456",
        "limit_contracts": 5,
        "search_query": "test query",
        "region_filter": "Moscow",
        "date_from": "2024-01-01",
        "date_to": "2024-12-31",
        "price_min": 1000.0,
        "price_max": 50000.0,
        "confidence_threshold": 0.8
    }
    
    # Mock redis and celery
    with patch('app.api.endpoints.search.redis_client') as mock_redis, \
         patch('app.api.endpoints.search.execute_search_task') as mock_task:
        
        mock_task.delay.return_value = Mock(id="task-123")
        mock_redis.set = Mock()
        
        response = client.post("/api/search", json=search_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Check response structure
        assert "id" in data
        assert data["input_source"] == "test_source"
        assert data["ktru_code"] == "123456"
        assert data["limit_contracts"] == 5
        assert data["status"] == "pending"
        
        # Verify database operations were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        
        # Verify task was triggered
        mock_task.delay.assert_called_once()
        mock_redis.set.assert_called_once()
        
        return data["id"]

def test_create_search_invalid_date():
    """Test creating search with invalid date format"""
    search_data = {
        "input_source": "test_source",
        "date_from": "01-01-2024",  # Wrong format
        "date_to": "2024-12-31"
    }
    
    response = client.post("/api/search", json=search_data)
    
    # Should return validation error
    assert response.status_code == 422

@pytest.mark.integration
def test_get_search():
    """Test getting search details by ID"""
    # Create a test search request
    test_search = create_test_search_request()
    test_search.input_source = "test_source_2"
    test_search.limit_contracts = 10
    
    # Mock the database query to return our test search
    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=test_search)
    
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = test_search
    
    # Now get the search
    response = client.get(f"/api/search/{test_search.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == str(test_search.id)
    assert data["input_source"] == "test_source_2"
    assert data["limit_contracts"] == 10

@pytest.mark.integration
def test_get_search_not_found():
    """Test getting non-existent search"""
    non_existent_id = str(uuid.uuid4())
    
    # Mock the database query to return None (not found)
    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=None)
    
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = None
    
    response = client.get(f"/api/search/{non_existent_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.integration
def test_stop_search():
    """Test stopping a search"""
    # First create a search
    search_data = {
        "input_source": "test_source_3",
        "limit_contracts": 3
    }
    
    create_response = client.post("/api/search", json=search_data)
    search_id = create_response.json()["id"]
    
    # Stop the search
    response = client.post(f"/api/search/{search_id}/stop")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == f"Stop signal sent for search {search_id}"
    assert data["search_id"] == search_id

@pytest.mark.integration
def test_search_events_stream():
    """Test connecting to SSE stream"""
    # Create a test search request
    test_search = create_test_search_request()
    test_search.input_source = "test_source_4"
    test_search.limit_contracts = 2
    
    # Mock the database query to return our test search
    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=test_search)
    
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = test_search
    
    # Mock the SessionLocal for the SSE stream
    with patch('app.db.SessionLocal') as mock_session_local:
        mock_session = Mock()
        mock_session_local.return_value = mock_session
        
        # Mock the query in the SSE stream
        mock_session_query = Mock()
        mock_session_filter = Mock()
        mock_session_first = Mock(return_value=test_search)
        
        mock_session.query.return_value = mock_session_query
        mock_session_query.filter.return_value = mock_session_filter
        mock_session_filter.first.return_value = test_search
        mock_session.refresh = Mock()
        
        # Mock redis client
        with patch('app.api.endpoints.search.redis_client') as mock_redis:
            mock_redis.get.return_value = None
            
            # Connect to events stream
            with client.stream("GET", f"/api/search/{test_search.id}/events") as response:
                # Read first event
                lines = []
                for line in response.iter_lines():
                    if line:
                        lines.append(line)
                        if len(lines) >= 2:  # Get at least initial connection event
                            break
                
                # Should have received some events
                assert len(lines) > 0
                
                # Parse first event
                event_data = lines[0]
                assert event_data.startswith("data: ")
                
                # Remove "data: " prefix and parse JSON
                import json
                event_json = json.loads(event_data[6:])
                assert "status" in event_json
                assert event_json.get("search_id") == str(test_search.id)

@pytest.mark.integration
def test_search_events_not_found():
    """Test connecting to SSE stream for non-existent search"""
    non_existent_id = str(uuid.uuid4())
    
    # Mock the SessionLocal for the SSE stream
    with patch('app.db.SessionLocal') as mock_session_local:
        mock_session = Mock()
        mock_session_local.return_value = mock_session
        
        # Mock the query in the SSE stream to return None (not found)
        mock_session_query = Mock()
        mock_session_filter = Mock()
        mock_session_first = Mock(return_value=None)
        
        mock_session.query.return_value = mock_session_query
        mock_session_query.filter.return_value = mock_session_filter
        mock_session_filter.first.return_value = None
        
        with client.stream("GET", f"/api/search/{non_existent_id}/events") as response:
            # Read event
            lines = []
            for line in response.iter_lines():
                if line:
                    lines.append(line)
                    break
            
            # Should have error event
            assert len(lines) > 0
            
            import json
            event_json = json.loads(lines[0][6:])
            assert "error" in event_json
            assert "not found" in event_json["error"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])