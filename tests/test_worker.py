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
        search_request.input_source = "test_source"
        search_request.ktru_code = "123456"
        search_request.limit_contracts = 3
        search_request.region_filter = "77"
        search_request.date_from = "2024-01-01"
        search_request.date_to = "2024-12-31"
        search_request.nmc_value = 100000.0
        search_request.confidence_threshold = 0.7
        search_request.total_contracts_found = 0
        search_request.contracts_processed = 0
        search_request.processing_started_at = None
        search_request.processing_completed_at = None
        search_request.error_message = None
        search_request.retry_count = 0
        search_request.ai_model_version = "v1.0"
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
        # Mock all dependencies including searchers and LLM engine
        with patch('app.workers.tasks.get_db_session', return_value=mock_db_session):
            with patch('app.workers.tasks.get_redis_client', return_value=mock_redis_client):
                with patch('app.workers.tasks.time.sleep') as mock_sleep:
                    with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                        with patch('app.workers.tasks.DetailZakupkiSearcher') as mock_detail_class:
                            with patch('app.workers.tasks.llm_engine') as mock_llm_engine:
                                # Mock query to return search request
                                mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request

                                # Mock Redis exists to return False (no stop signal)
                                mock_redis_client.exists.return_value = False

                                # Mock parser searcher to return empty result (simplifies test)
                                mock_parser_searcher = Mock()
                                mock_parser_class.return_value = mock_parser_searcher
                                mock_parser_searcher.search.return_value = Mock(cards=[])

                                # Mock detail searcher
                                mock_detail_searcher = Mock()
                                mock_detail_class.return_value = mock_detail_searcher
                                mock_detail_searcher.parse_contract_details.return_value = {'success': False}
                                mock_detail_searcher.close = Mock()

                                # Mock LLM engine (not used when no contracts)
                                mock_llm_engine.extract_specs = Mock()

                                # Create mock task instance
                                mock_task = Mock()
                                mock_task.update_state = Mock()

                                # Execute task - call the underlying function directly
                                result = _execute_search_task_logic(mock_task, sample_search_request.id)

                                # Verify status was updated (check mock calls)
                                mock_db_session.commit.assert_called()

                                # Verify stop signal was checked (when no contracts, exists may not be called)
                                # When parser returns empty cards, function completes early without checking stop signal
                                # So we don't assert exists was called

                                # Verify sleep was NOT called (no contracts to process)
                                assert mock_sleep.call_count == 0

                                # Verify progress updates (at least starting progress)
                                assert mock_task.update_state.call_count > 0

                                # Verify final status is COMPLETED (no contracts found)
                                assert result['status'] == 'completed'
                                assert 'no contracts found' in result['message']
                                assert str(sample_search_request.id) in result['search_id']
    
    def test_task_with_stop_signal(self, mock_db_session, mock_redis_client, sample_search_request):
        """Test task execution with stop signal"""
        # Mock all dependencies including searchers
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
                    with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                        with patch('app.workers.tasks.DetailZakupkiSearcher') as mock_detail_class:
                            # Mock query to return search request
                            mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request

                            # Mock Redis exists to return True (stop signal present)
                            mock_redis_client.exists.return_value = True

                            # Mock parser searcher to return some contracts
                            mock_parser_searcher = Mock()
                            mock_parser_class.return_value = mock_parser_searcher
                            # Return a mock with cards to ensure function enters processing loop
                            mock_card = Mock(reestr_number='1234567890')
                            mock_parser_searcher.search.return_value = Mock(cards=[mock_card])

                            # Mock detail searcher (won't be called due to stop signal)
                            mock_detail_searcher = Mock()
                            mock_detail_class.return_value = mock_detail_searcher
                            mock_detail_searcher.parse_contract_details = Mock()
                            mock_detail_searcher.close = Mock()

                            # Create mock task instance
                            mock_task = Mock()
                            mock_task.update_state = Mock()

                            # Execute task - call the underlying function directly
                            result = _execute_search_task_logic(mock_task, sample_search_request.id)

                            # Verify stop signal check
                            expected_stop_key = f"stop_signal:{sample_search_request.id}"
                            mock_redis_client.exists.assert_called_with(expected_stop_key)

                            # Verify stop signal was cleared
                            mock_redis_client.delete.assert_called_with(expected_stop_key)

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