"""
Unit tests for the report_generator.py module.
"""

import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO

from app.services.report_generator import ReportGenerator
from app.models.contract import ContractResult, SpecComparisonRow, MatchType, MatchStatus
from app.models.search import SearchRequest, SearchStatus


class TestReportGenerator:
    """Test cases for ReportGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock(spec=Session)
        self.report_generator = ReportGenerator(self.mock_db)
        self.search_id = uuid.uuid4()
        
        # Mock search request
        self.mock_search = Mock(spec=SearchRequest)
        self.mock_search.id = self.search_id
        self.mock_search.input_source = "test_source"
        self.mock_search.ktru_code = "123456"
        self.mock_search.search_query = "test query"
        self.mock_search.region_filter = "Moscow"
        self.mock_search.date_from = "2024-01-01"
        self.mock_search.date_to = "2024-12-31"
        self.mock_search.price_min = 1000.0
        self.mock_search.price_max = 50000.0
        self.mock_search.nmc_value = 25000.0
        self.mock_search.ai_model_version = "v1.0"
        self.mock_search.confidence_threshold = 0.7
        self.mock_search.status = SearchStatus.COMPLETED.value
    
    def test_get_nmcc_calculation_no_contracts(self):
        """Test NMCC calculation when no contracts exist."""
        # Mock query to return no contracts
        mock_query = Mock()
        mock_query.filter.return_value.filter.return_value.order_by.return_value.all.return_value = []
        mock_query.filter.return_value.count.return_value = 0
        self.mock_db.query.return_value = mock_query
        
        result = self.report_generator.get_nmcc_calculation(self.search_id)
        
        assert result['nmcc_value'] is None
        assert result['top_contracts'] == []
        assert result['total_contracts'] == 0
        assert result['contracts_with_flag'] == 0
        assert result['search_id'] == str(self.search_id)
        assert 'calculation_date' in result
    
    def test_get_nmcc_calculation_with_contracts(self):
        """Test NMCC calculation with contracts."""
        # Create mock contracts
        mock_contracts = []
        for i in range(5):
            contract = Mock(spec=ContractResult)
            contract.reestr_number = f"REESTR-{i}"
            contract.contract_number = f"CONTRACT-{i}"
            contract.supplier_name = f"Supplier {i}"
            contract.contract_price = 10000.0 * (i + 1)  # 10000, 20000, 30000, 40000, 50000
            contract.currency = "RUB"
            contract.ai_score = 0.9 - (i * 0.1)  # 0.9, 0.8, 0.7, 0.6, 0.5
            contract.match_type = MatchType.EXACT
            contract.contract_date = "2024-01-01"
            mock_contracts.append(contract)
        
        # Mock queries
        mock_query = Mock()
        mock_query.filter.return_value.filter.return_value.order_by.return_value.all.return_value = mock_contracts
        mock_query.filter.return_value.count.return_value = 10  # total contracts
        self.mock_db.query.return_value = mock_query
        
        result = self.report_generator.get_nmcc_calculation(self.search_id)
        
        # Should return top 3 contracts (highest ai_score)
        assert len(result['top_contracts']) == 3
        assert result['top_contracts'][0]['ai_score'] == 0.9  # Highest score
        assert result['top_contracts'][1]['ai_score'] == 0.8
        assert result['top_contracts'][2]['ai_score'] == 0.7
        
        # NMCC should be average of top 3 contract prices: (10000 + 20000 + 30000) / 3 = 20000
        assert result['nmcc_value'] == 20000.0
        assert result['total_contracts'] == 10
        assert result['contracts_with_flag'] == 5
    
    def test_get_nmcc_calculation_with_none_prices(self):
        """Test NMCC calculation when some contracts have None prices."""
        # Create mock contracts with some None prices
        mock_contracts = []
        for i in range(3):
            contract = Mock(spec=ContractResult)
            contract.reestr_number = f"REESTR-{i}"
            contract.contract_number = f"CONTRACT-{i}"
            contract.supplier_name = f"Supplier {i}"
            contract.contract_price = 10000.0 * (i + 1) if i < 2 else None  # 10000, 20000, None
            contract.currency = "RUB"
            contract.ai_score = 0.9 - (i * 0.1)
            contract.match_type = MatchType.EXACT
            contract.contract_date = "2024-01-01"
            mock_contracts.append(contract)
        
        # Mock queries
        mock_query = Mock()
        mock_query.filter.return_value.filter.return_value.order_by.return_value.all.return_value = mock_contracts
        mock_query.filter.return_value.count.return_value = 3
        self.mock_db.query.return_value = mock_query
        
        result = self.report_generator.get_nmcc_calculation(self.search_id)
        
        # NMCC should be average of valid prices only: (10000 + 20000) / 2 = 15000
        assert result['nmcc_value'] == 15000.0
    
    def test_generate_comparison_matrix_empty(self):
        """Test comparison matrix generation with no contracts."""
        result = self.report_generator.generate_comparison_matrix(self.search_id, [])
        
        assert result.empty
    
    def test_generate_comparison_matrix_with_data(self):
        """Test comparison matrix generation with contract data."""
        # Mock top contracts
        top_contracts = [
            {
                'reestr_number': 'REESTR-001',
                'contract_number': 'CONTRACT-001',
                'supplier_name': 'Supplier 1',
                'contract_price': 10000.0,
                'currency': 'RUB',
                'ai_score': 0.9,
                'match_type': 'exact',
                'contract_date': '2024-01-01',
                'rank': 1
            },
            {
                'reestr_number': 'REESTR-002',
                'contract_number': 'CONTRACT-002',
                'supplier_name': 'Supplier 2',
                'contract_price': 20000.0,
                'currency': 'RUB',
                'ai_score': 0.8,
                'match_type': 'partial',
                'contract_date': '2024-01-02',
                'rank': 2
            }
        ]
        
        # Mock contract objects
        mock_contract1 = Mock(spec=ContractResult)
        mock_contract1.id = uuid.uuid4()
        mock_contract1.reestr_number = 'REESTR-001'
        
        mock_contract2 = Mock(spec=ContractResult)
        mock_contract2.id = uuid.uuid4()
        mock_contract2.reestr_number = 'REESTR-002'
        
        # Mock spec comparison rows
        mock_spec1 = Mock(spec=SpecComparisonRow)
        mock_spec1.name = 'Weight'
        mock_spec1.actual_value = '100 kg'
        mock_spec1.target_value = '100 kg'
        mock_spec1.match_status = MatchStatus.MATCH
        
        mock_spec2 = Mock(spec=SpecComparisonRow)
        mock_spec2.name = 'Color'
        mock_spec2.actual_value = 'Red'
        mock_spec2.target_value = 'Blue'
        mock_spec2.match_status = MatchStatus.MISMATCH
        
        mock_spec3 = Mock(spec=SpecComparisonRow)
        mock_spec3.name = 'Material'
        mock_spec3.actual_value = 'Steel'
        mock_spec3.target_value = 'Steel'
        mock_spec3.match_status = MatchStatus.MATCH
        
        # Mock queries
        def mock_query_side_effect(model):
            mock_query_obj = Mock()
            
            if model == ContractResult:
                # First call: filter by search_id and reestr_number for contract1
                # Second call: filter by search_id and reestr_number for contract2
                # We'll handle this with a simple approach
                if hasattr(mock_query_obj, 'call_count'):
                    mock_query_obj.call_count += 1
                else:
                    mock_query_obj.call_count = 0
                
                if mock_query_obj.call_count == 0:
                    mock_query_obj.filter.return_value.filter.return_value.first.return_value = mock_contract1
                else:
                    mock_query_obj.filter.return_value.filter.return_value.first.return_value = mock_contract2
            elif model == SpecComparisonRow:
                # Return all spec rows
                mock_query_obj.filter.return_value.all.return_value = [mock_spec1, mock_spec2, mock_spec3]
            
            return mock_query_obj
        
        self.mock_db.query.side_effect = mock_query_side_effect
        
        # Also need to mock the query for contract IDs
        with patch.object(self.mock_db.query.return_value.filter.return_value, 'all', return_value=[mock_spec1, mock_spec2, mock_spec3]):
            result = self.report_generator.generate_comparison_matrix(self.search_id, top_contracts)
        
        # Check result
        assert not result.empty
        assert 'Specification' in result.columns
        assert len(result) == 3  # 3 specifications
    
    def test_create_xlsx_report_success(self):
        """Test XLSX report creation."""
        # Mock search query
        mock_search_query = Mock()
        mock_search_query.filter.return_value.first.return_value = self.mock_search
        self.mock_db.query.return_value = mock_search_query
        
        # Mock get_nmcc_calculation to return test data
        test_nmcc_data = {
            'nmcc_value': 20000.0,
            'top_contracts': [
                {
                    'rank': 1,
                    'reestr_number': 'REESTR-001',
                    'contract_number': 'CONTRACT-001',
                    'supplier_name': 'Supplier 1',
                    'contract_price': 10000.0,
                    'currency': 'RUB',
                    'ai_score': 0.9,
                    'match_type': 'exact',
                    'contract_date': '2024-01-01'
                }
            ],
            'total_contracts': 10,
            'contracts_with_flag': 5,
            'search_id': str(self.search_id),
            'calculation_date': datetime.now().isoformat()
        }
        
        # Mock generate_comparison_matrix to return empty DataFrame
        empty_df = pd.DataFrame()
        
        with patch.object(self.report_generator, 'get_nmcc_calculation', return_value=test_nmcc_data), \
             patch.object(self.report_generator, 'generate_comparison_matrix', return_value=empty_df):
            
            xlsx_file = self.report_generator.create_xlsx_report(self.search_id)
            
            # Verify file is created
            assert isinstance(xlsx_file, BytesIO)
            
            # Load and verify workbook
            xlsx_file.seek(0)
            wb = load_workbook(xlsx_file)
            
            # Check sheets
            assert 'Summary' in wb.sheetnames
            if not empty_df.empty:
                assert 'Comparison Matrix' in wb.sheetnames
            
            # Check summary sheet content
            ws_summary = wb['Summary']
            assert ws_summary['A1'].value == f"NMCC Calculation Report - Search ID: {self.search_id}"
            assert ws_summary['B5'].value == 20000.0  # NMCC value
            assert ws_summary['B7'].value == 10  # Total contracts
            assert ws_summary['B8'].value == 5  # Contracts with flag
    
    def test_generate_report_success(self):
        """Test generate_report method."""
        # Mock create_xlsx_report
        mock_xlsx = BytesIO(b'test xlsx content')
        with patch.object(self.report_generator, 'create_xlsx_report', return_value=mock_xlsx):
            xlsx_file, filename = self.report_generator.generate_report(self.search_id)
            
            assert xlsx_file == mock_xlsx
            assert filename.startswith(f"nmcc_report_{self.search_id}_")
            assert filename.endswith('.xlsx')