import uuid
import time
import pytest
import redis
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.workers.tasks import _execute_search_task_logic
from app.models.search import SearchRequest, SearchStatus
from app.core.config import settings


class TestExecuteSearchTask:
    """Test suite for execute_search_task Celery task"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        mock_session = Mock(spec=Session)
        return mock_session
    
    @pytest.fixture
    def mock_redis_client(self):
        """Mock Redis client"""
        mock_redis = Mock(spec=redis.Redis)
        return mock_redis
    
    @pytest.fixture
    def sample_search_id(self):
        """Sample search ID for testing"""
        return uuid.uuid4()
    
    @pytest.fixture
    def sample_search_request(self, sample_search_id):
        """Sample search request for testing"""
        search_request = Mock(spec=SearchRequest)
        search_request.id = sample_search_id
        search_request.status = SearchStatus.PENDING
        return search_request
    
    def test_task_with_nonexistent_search_id(self, mock_db_session, mock_redis_client):
        """Test task execution with non-existent search ID"""
        # Mock dependencies
        with patch('app.workers.tasks.get_db_session', return_value=mock_db_session):
            with patch('app.workers.tasks.get_redis_client', return_value=mock_redis_client):
                # Mock query to return None (search not found)
                mock_db_session.query.return_value.filter.return_value.first.return_value = None
                
                # Create mock task instance
                mock_task = Mock()
                mock_task.update_state = Mock()
                
                # Execute task - call the underlying function directly
                search_id = uuid.uuid4()
                result = _execute_search_task_logic(mock_task, search_id)
                
                # Verify error handling
                mock_task.update_state.assert_called_once_with(
                    state='FAILURE',
                    meta={'error': f'Search request {search_id} not found'}
                )
                assert result['status'] == 'error'
                assert f'Search request {search_id} not found' in result['message']
    
    def test_task_successful_execution(self, mock_db_session, mock_redis_client, sample_search_request):
        """Test successful task execution without stop signal"""
        # Mock dependencies
        with patch('app.workers.tasks.get_db_session', return_value=mock_db_session):
            with patch('app.workers.tasks.get_redis_client', return_value=mock_redis_client):
                with patch('app.workers.tasks.time.sleep') as mock_sleep:
                    # Mock query to return search request
                    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                    
                    # Mock Redis exists to return False (no stop signal)
                    mock_redis_client.exists.return_value = False
                    
                    # Create mock task instance
                    mock_task = Mock()
                    mock_task.update_state = Mock()
                    
                    # Execute task - call the underlying function directly
                    result = _execute_search_task_logic(mock_task, sample_search_request.id)
                    
                    # Verify status was updated to PROCESSING (check mock calls)
                    # The status is set to PROCESSING then COMPLETED, so we check the mock was called
                    mock_db_session.commit.assert_called()
                    
                    # Verify stop signal was checked
                    expected_stop_key = f"stop_signal:{sample_search_request.id}"
                    mock_redis_client.exists.assert_called_with(expected_stop_key)
                    
                    # Verify sleep was called (simulating work)
                    assert mock_sleep.call_count > 0
                    
                    # Verify progress updates
                    assert mock_task.update_state.call_count > 0
                    
                    # Verify final status update to COMPLETED
                    assert sample_search_request.status == SearchStatus.COMPLETED
                    
                    # Verify result
                    assert result['status'] == 'completed'
                    assert 'completed successfully' in result['message']
                    assert str(sample_search_request.id) in result['search_id']
    
    def test_task_with_stop_signal(self, mock_db_session, mock_redis_client, sample_search_request):
        """Test task execution with stop signal"""
        # Mock dependencies
        with patch('app.workers.tasks.get_db_session', return_value=mock_db_session):
            with patch('app.workers.tasks.get_redis_client', return_value=mock_redis_client):
                with patch('app.workers.tasks.time.sleep') as mock_sleep:
                    # Mock query to return search request
                    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                    
                    # Mock Redis exists to return True (stop signal present)
                    mock_redis_client.exists.return_value = True
                    
                    # Create mock task instance
                    mock_task = Mock()
                    mock_task.update_state = Mock()
                    
                    # Execute task - call the underlying function directly
                    result = _execute_search_task_logic(mock_task, sample_search_request.id)
                    
                    # Verify stop signal was checked
                    expected_stop_key = f"stop_signal:{sample_search_request.id}"
                    mock_redis_client.exists.assert_called_with(expected_stop_key)
                    
                    # Verify status was updated to CANCELLED
                    assert sample_search_request.status == SearchStatus.CANCELLED
                    
                    # Verify stop signal was cleared
                    mock_redis_client.delete.assert_called_with(f"stop_signal:{sample_search_request.id}")
                    
                    # Verify result
                    assert result['status'] == 'cancelled'
                    assert 'cancelled by stop signal' in result['message']
                    assert 'progress' in result
    
    def test_task_database_error(self, mock_db_session, mock_redis_client):
        """Test task execution with database error"""
        # Mock dependencies
        with patch('app.workers.tasks.get_db_session', return_value=mock_db_session):
            with patch('app.workers.tasks.get_redis_client', return_value=mock_redis_client):
                # Mock query to raise an exception
                mock_db_session.query.side_effect = Exception("Database connection failed")
                
                # Create mock task instance
                mock_task = Mock()
                mock_task.update_state = Mock()
                
                # Execute task - call the underlying function directly
                search_id = uuid.uuid4()
                result = _execute_search_task_logic(mock_task, search_id)
                
                # Verify error handling
                mock_task.update_state.assert_called_once_with(
                    state='FAILURE',
                    meta={'error': 'Database connection failed'}
                )
                assert result['status'] == 'error'
                assert 'Unexpected error' in result['message']


class TestIntegration:
    """Integration tests for worker tasks"""
    
    @pytest.mark.integration
    def test_redis_stop_signal_workflow(self):
        """Integration test for Redis stop signal workflow"""
        # This test requires Redis to be running
        try:
            redis_client = redis.Redis.from_url(settings.REDIS_URL)
            redis_client.ping()
        except redis.ConnectionError:
            pytest.skip("Redis not available for integration test")
        
        # Create a test search ID
        test_search_id = uuid.uuid4()
        stop_signal_key = f"stop_signal:{test_search_id}"
        
        # Set stop signal
        redis_client.set(stop_signal_key, "1")
        
        # Verify stop signal exists
        assert redis_client.exists(stop_signal_key) == 1
        
        # Clear stop signal
        redis_client.delete(stop_signal_key)
        
        # Verify stop signal is cleared
        assert redis_client.exists(stop_signal_key) == 0
        
        # Clean up
        redis_client.close()
    
    @pytest.mark.integration  
    def test_task_state_transitions(self):
        """Integration test for task state transitions"""
        # This test would require a running Celery worker and database
        # For now, we'll skip it and rely on unit tests
        pytest.skip("Integration test requires running Celery worker and database")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])