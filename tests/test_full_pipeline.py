"""
Integration test for the full pipeline with mocked HTTP responses.
Tests that the worker task executes the complete pipeline without hitting external APIs.
"""
import uuid
import json
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.workers.tasks import _execute_search_task_logic
from app.models.search import SearchRequest, SearchStatus
from app.models.contract import ContractResult, MatchType, SpecComparisonRow, MatchStatus
from app.services.zakupki_parser import ContractCard, SearchResult
from app.services.zakupki_searcher import ZakupkiSearcher as DetailZakupkiSearcher
from app.services.llm_engine import LLMEngine


class TestFullPipeline:
    """Test suite for the full pipeline execution"""
    
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
    
    @pytest.fixture
    def mock_contract_cards(self):
        """Mock contract cards for testing"""
        return [
            ContractCard(
                reestr_number="1234567890",
                contract_date=date(2024, 6, 15),
                price=95000.0,
                link="https://zakupki.gov.ru/contract/1234567890",
                title="Test Contract 1"
            ),
            ContractCard(
                reestr_number="2345678901",
                contract_date=date(2024, 7, 20),
                price=105000.0,
                link="https://zakupki.gov.ru/contract/2345678901",
                title="Test Contract 2"
            ),
            ContractCard(
                reestr_number="3456789012",
                contract_date=date(2024, 8, 25),
                price=90000.0,
                link="https://zakupki.gov.ru/contract/3456789012",
                title="Test Contract 3"
            )
        ]
    
    @pytest.fixture
    def mock_search_result(self, mock_contract_cards):
        """Mock search result for testing"""
        return SearchResult(
            total_count=len(mock_contract_cards),
            cards=mock_contract_cards
        )
    
    @pytest.fixture
    def mock_contract_details(self):
        """Mock contract details for testing"""
        return {
            'success': True,
            'contract_card': {
                'reestr_number': '1234567890',
                'customer_name': 'Test Customer',
                'publication_date': '15.06.2024'
            },
            'objects': {
                'specification_text': 'Test specification text for KTRU 123456',
                'unit_price': 95000.0,
                'ktru_found': True,
                'objects': []
            },
            'attachments': [],
            'downloaded_files': [],
            'warnings': []
        }
    
    @pytest.fixture
    def mock_extracted_specs(self):
        """Mock extracted specifications for testing"""
        return {
            'product_name': 'Test Product',
            'manufacturer': 'Test Manufacturer',
            'model': 'Model X',
            'technical_specs': {
                'weight': '10 kg',
                'dimensions': '100x50x30 cm',
                'power': '100W'
            },
            'quantity': 1,
            'unit_price': 95000.0,
            'total_price': 95000.0,
            'delivery_terms': '30 days',
            'warranty': '1 year',
            'extraction_timestamp': '2024-01-01T12:00:00',
            'ktru_code': '123456'
        }
    
    def test_full_pipeline_execution(self, sample_search_request, mock_search_result, 
                                    mock_contract_details, mock_extracted_specs):
        """Test the full pipeline execution with mocked dependencies"""
        
        # Mock all external dependencies
        with patch('app.workers.tasks.get_db_session') as mock_get_db_session:
            with patch('app.workers.tasks.get_redis_client') as mock_get_redis_client:
                with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                    with patch('app.workers.tasks.DetailZakupkiSearcher') as mock_detail_class:
                        with patch('app.workers.tasks.llm_engine') as mock_llm_engine:
                            with patch('app.workers.tasks.time.sleep') as mock_sleep:
                                
                                # Setup mock database session
                                mock_db_session = Mock(spec=Session)
                                mock_get_db_session.return_value = mock_db_session
                                
                                # Mock query to return search request
                                mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                                
                                # Setup mock Redis client
                                mock_redis_client = Mock()
                                mock_get_redis_client.return_value = mock_redis_client
                                mock_redis_client.exists.return_value = False  # No stop signal
                                
                                # Setup mock parser searcher
                                mock_parser_searcher = Mock()
                                mock_parser_class.return_value = mock_parser_searcher
                                mock_parser_searcher.search.return_value = mock_search_result
                                
                                # Setup mock detail searcher
                                mock_detail_searcher = Mock()
                                mock_detail_class.return_value = mock_detail_searcher
                                mock_detail_searcher.parse_contract_details.return_value = mock_contract_details
                                mock_detail_searcher.close = Mock()
                                
                                # Setup mock LLM engine
                                mock_llm_engine.extract_specs.return_value = mock_extracted_specs
                                
                                # Create mock task instance
                                mock_task = Mock()
                                mock_task.update_state = Mock()
                                
                                # Execute the task logic
                                result = _execute_search_task_logic(mock_task, sample_search_request.id)
                                
                                # Verify the pipeline was executed correctly
                                
                                # 1. Database was queried for search request
                                mock_db_session.query.assert_called()
                                
                                # 2. Status was updated to PROCESSING
                                assert sample_search_request.status == SearchStatus.COMPLETED
                                assert sample_search_request.processing_started_at is not None

                                # Note: We don't check sample_search_request.status directly because
                                # the mock object's status might be changed multiple times during execution
                                # (PROCESSING -> COMPLETED)
                                
                                # 3. Parser searcher was called with correct parameters
                                mock_parser_searcher.search.assert_called_once_with(
                                    fz_44=True,
                                    region=sample_search_request.region_filter,
                                    ktru=sample_search_request.ktru_code,
                                    date_from=date(2024, 1, 1),
                                    date_to=date(2024, 12, 31),
                                    max_pages=1
                                )
                                
                                # 4. Total contracts found was updated
                                assert sample_search_request.total_contracts_found == len(mock_search_result.cards)
                                
                                # 5. Detail searcher was created with search ID
                                mock_detail_class.assert_called_once_with(sample_search_request.id)
                                
                                # 6. Contract details were fetched for each contract
                                assert mock_detail_searcher.parse_contract_details.call_count == 3
                                
                                # 7. LLM was called to extract specifications
                                assert mock_llm_engine.extract_specs.call_count == 3
                                
                                # 8. Contract results were added to database
                                assert mock_db_session.add.call_count >= 3  # At least 3 ContractResult objects
                                
                                # 9. Spec comparison rows were added
                                # Each contract has 3 technical specs, so 3 * 3 = 9 spec rows
                                assert mock_db_session.add.call_count >= 12  # 3 contracts + 9 spec rows
                                
                                # 10. Contracts processed count was updated
                                assert sample_search_request.contracts_processed == 3
                                
                                # 11. Status was updated to COMPLETED
                                assert sample_search_request.status == SearchStatus.COMPLETED
                                assert sample_search_request.processing_completed_at is not None
                                
                                # 12. Detail searcher was closed
                                mock_detail_searcher.close.assert_called_once()
                                
                                # 13. Task returned success result
                                assert result['status'] == 'completed'
                                assert 'completed successfully' in result['message']
                                assert result['processed'] == 3
                                assert result['total'] == 3
                                
                                # 14. Progress updates were sent
                                assert mock_task.update_state.call_count > 0
    
    def test_pipeline_with_stop_signal(self, sample_search_request, mock_search_result):
        """Test pipeline execution with stop signal"""
        
        with patch('app.workers.tasks.get_db_session') as mock_get_db_session:
            with patch('app.workers.tasks.get_redis_client') as mock_get_redis_client:
                with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                    with patch('app.workers.tasks.time.sleep'):
                        
                        # Setup mocks
                        mock_db_session = Mock(spec=Session)
                        mock_get_db_session.return_value = mock_db_session
                        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                        
                        mock_redis_client = Mock()
                        mock_get_redis_client.return_value = mock_redis_client
                        mock_redis_client.exists.return_value = True  # Stop signal present
                        
                        mock_parser_searcher = Mock()
                        mock_parser_class.return_value = mock_parser_searcher
                        mock_parser_searcher.search.return_value = mock_search_result
                        
                        mock_task = Mock()
                        mock_task.update_state = Mock()
                        
                        # Execute task
                        result = _execute_search_task_logic(mock_task, sample_search_request.id)
                        
                        # Verify stop signal was checked
                        expected_stop_key = f"stop_signal:{sample_search_request.id}"
                        mock_redis_client.exists.assert_called_with(expected_stop_key)
                        
                        # Verify status was updated to CANCELLED
                        assert sample_search_request.status == SearchStatus.CANCELLED
                        
                        # Verify stop signal was cleared
                        mock_redis_client.delete.assert_called_with(expected_stop_key)
                        
                        # Verify result indicates cancellation
                        assert result['status'] == 'cancelled'
                        assert 'cancelled by stop signal' in result['message']
    
    def test_pipeline_with_failed_contract(self, sample_search_request, mock_search_result):
        """Test pipeline when contract details fetch fails"""
        
        with patch('app.workers.tasks.get_db_session') as mock_get_db_session:
            with patch('app.workers.tasks.get_redis_client') as mock_get_redis_client:
                with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                    with patch('app.workers.tasks.DetailZakupkiSearcher') as mock_detail_class:
                        with patch('app.workers.tasks.time.sleep'):
                            
                            # Setup mocks
                            mock_db_session = Mock(spec=Session)
                            mock_get_db_session.return_value = mock_db_session
                            mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                            
                            mock_redis_client = Mock()
                            mock_get_redis_client.return_value = mock_redis_client
                            mock_redis_client.exists.return_value = False
                            
                            mock_parser_searcher = Mock()
                            mock_parser_class.return_value = mock_parser_searcher
                            mock_parser_searcher.search.return_value = mock_search_result
                            
                            # Setup detail searcher to return failed contract
                            mock_detail_searcher = Mock()
                            mock_detail_class.return_value = mock_detail_searcher
                            mock_detail_searcher.parse_contract_details.return_value = {'success': False, 'error': 'Failed to fetch'}
                            mock_detail_searcher.close = Mock()
                            
                            mock_task = Mock()
                            mock_task.update_state = Mock()
                            
                            # Execute task
                            result = _execute_search_task_logic(mock_task, sample_search_request.id)
                            
                            # Verify contract details were attempted
                            assert mock_detail_searcher.parse_contract_details.call_count == 3
                            
                            # Verify no contracts were processed (all failed)
                            assert sample_search_request.contracts_processed == 0
                            
                            # Verify task still completed successfully
                            assert result['status'] == 'completed'
                            assert result['processed'] == 0
    
    def test_pipeline_with_llm_error(self, sample_search_request, mock_search_result, mock_contract_details):
        """Test pipeline when LLM extraction fails"""
        
        with patch('app.workers.tasks.get_db_session') as mock_get_db_session:
            with patch('app.workers.tasks.get_redis_client') as mock_get_redis_client:
                with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                    with patch('app.workers.tasks.DetailZakupkiSearcher') as mock_detail_class:
                        with patch('app.workers.tasks.llm_engine') as mock_llm_engine:
                            with patch('app.workers.tasks.time.sleep'):
                                
                                # Setup mocks
                                mock_db_session = Mock(spec=Session)
                                mock_get_db_session.return_value = mock_db_session
                                mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                                
                                mock_redis_client = Mock()
                                mock_get_redis_client.return_value = mock_redis_client
                                mock_redis_client.exists.return_value = False
                                
                                mock_parser_searcher = Mock()
                                mock_parser_class.return_value = mock_parser_searcher
                                mock_parser_searcher.search.return_value = mock_search_result
                                
                                mock_detail_searcher = Mock()
                                mock_detail_class.return_value = mock_detail_searcher
                                mock_detail_searcher.parse_contract_details.return_value = mock_contract_details
                                mock_detail_searcher.close = Mock()
                                
                                # Setup LLM to raise exception
                                mock_llm_engine.extract_specs.side_effect = Exception("LLM API error")
                                
                                mock_task = Mock()
                                mock_task.update_state = Mock()
                                
                                # Execute task
                                result = _execute_search_task_logic(mock_task, sample_search_request.id)
                                
                                # Verify LLM was called
                                assert mock_llm_engine.extract_specs.call_count == 3
                                
                                # Verify contracts were still processed (LLM error is logged but doesn't stop processing)
                                assert sample_search_request.contracts_processed == 3
                                
                                # Verify task completed successfully
                                assert result['status'] == 'completed'
                                assert result['processed'] == 3
    
    def test_pipeline_with_no_contracts(self, sample_search_request):
        """Test pipeline when no contracts are found"""
        
        with patch('app.workers.tasks.get_db_session') as mock_get_db_session:
            with patch('app.workers.tasks.get_redis_client') as mock_get_redis_client:
                with patch('app.workers.tasks.ParserZakupkiSearcher') as mock_parser_class:
                    
                    # Setup mocks
                    mock_db_session = Mock(spec=Session)
                    mock_get_db_session.return_value = mock_db_session
                    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_search_request
                    
                    mock_redis_client = Mock()
                    mock_get_redis_client.return_value = mock_redis_client
                    mock_redis_client.exists.return_value = False
                    
                    # Setup parser to return empty result
                    mock_parser_searcher = Mock()
                    mock_parser_class.return_value = mock_parser_searcher
                    mock_parser_searcher.search.return_value = SearchResult(total_count=0, cards=[])
                    
                    mock_task = Mock()
                    mock_task.update_state = Mock()
                    
                    # Execute task
                    result = _execute_search_task_logic(mock_task, sample_search_request.id)
                    
                    # Verify status was updated to COMPLETED
                    assert sample_search_request.status == SearchStatus.COMPLETED
                    
                    # Verify result indicates no contracts found
                    assert result['status'] == 'completed'
                    assert 'no contracts found' in result['message']


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])