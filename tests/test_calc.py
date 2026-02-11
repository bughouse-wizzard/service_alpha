"""
Tests for NMTSK calculation service.
"""

import os
import tempfile
from decimal import Decimal
from datetime import datetime, timezone
import uuid

import pytest

from app.services.calc import (
    calculate_nmtsk_average,
    calculate_nmtsk_average_from_responses,
    generate_excel_report
)
from app.models import ContractResult, SearchRequest, SearchStatus
from app.schemas import ContractResultResponse


class TestNMTSKCalculation:
    """Test NMTSK calculation logic."""
    
    def test_calculate_nmtsk_average_with_three_contracts(self):
        """Test average calculation with exactly 3 contracts."""
        # Create dummy contracts with prices
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
            self._create_dummy_contract(unit_price=Decimal('2000.00')),
            self._create_dummy_contract(unit_price=Decimal('3000.00')),
        ]
        
        # Calculate average - should take top 3 (all of them) and average
        result = calculate_nmtsk_average(contracts)
        
        # Expected: (3000 + 2000 + 1000) / 3 = 2000
        assert result == Decimal('2000.00')
    
    def test_calculate_nmtsk_average_with_more_than_three_contracts(self):
        """Test average calculation with more than 3 contracts - should take top 3."""
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('500.00')),
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
            self._create_dummy_contract(unit_price=Decimal('1500.00')),
            self._create_dummy_contract(unit_price=Decimal('2000.00')),
            self._create_dummy_contract(unit_price=Decimal('2500.00')),
        ]
        
        # Should take top 3: 2500, 2000, 1500
        result = calculate_nmtsk_average(contracts)
        
        # Expected: (2500 + 2000 + 1500) / 3 = 2000
        assert result == Decimal('2000.00')
    
    def test_calculate_nmtsk_average_with_fewer_than_three_contracts(self):
        """Test average calculation with fewer than 3 contracts."""
        # Test with 2 contracts
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
            self._create_dummy_contract(unit_price=Decimal('2000.00')),
        ]
        
        result = calculate_nmtsk_average(contracts)
        
        # Expected: (2000 + 1000) / 2 = 1500
        assert result == Decimal('1500.00')
        
        # Test with 1 contract
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1500.00')),
        ]
        
        result = calculate_nmtsk_average(contracts)
        
        # Expected: 1500 / 1 = 1500
        assert result == Decimal('1500.00')
    
    def test_calculate_nmtsk_average_with_no_prices(self):
        """Test average calculation when no contracts have prices."""
        contracts = [
            self._create_dummy_contract(unit_price=None),
            self._create_dummy_contract(unit_price=None),
        ]
        
        result = calculate_nmtsk_average(contracts)
        
        assert result is None
    
    def test_calculate_nmtsk_average_with_mixed_prices(self):
        """Test average calculation when some contracts don't have prices."""
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
            self._create_dummy_contract(unit_price=None),  # No price
            self._create_dummy_contract(unit_price=Decimal('3000.00')),
            self._create_dummy_contract(unit_price=Decimal('2000.00')),
        ]
        
        # Should take top 3 with prices: 3000, 2000, 1000
        result = calculate_nmtsk_average(contracts)
        
        assert result == Decimal('2000.00')
    
    def test_calculate_nmtsk_average_with_empty_list(self):
        """Test average calculation with empty contracts list."""
        result = calculate_nmtsk_average([])
        
        assert result is None
    
    def test_calculate_nmtsk_average_from_responses(self):
        """Test average calculation using ContractResultResponse objects."""
        # Create dummy responses
        responses = [
            ContractResultResponse(
                id=str(uuid.uuid4()),
                search_id=str(uuid.uuid4()),
                reestr_number="123",
                unit_price=Decimal('1000.00'),
                match_type="exact",
            ),
            ContractResultResponse(
                id=str(uuid.uuid4()),
                search_id=str(uuid.uuid4()),
                reestr_number="456",
                unit_price=Decimal('2000.00'),
                match_type="partial",
            ),
            ContractResultResponse(
                id=str(uuid.uuid4()),
                search_id=str(uuid.uuid4()),
                reestr_number="789",
                unit_price=Decimal('3000.00'),
                match_type="similar",
            ),
        ]
        
        result = calculate_nmtsk_average_from_responses(responses)
        
        assert result == Decimal('2000.00')
    
    def _create_dummy_contract(self, unit_price=None):
        """Helper to create a dummy ContractResult object."""
        search_request = SearchRequest(
            id=str(uuid.uuid4()),
            input_source="test",
            object_name="Test Object",
            status=SearchStatus.COMPLETED,
            found_total=5,
            processed_count=5,
            nmc_value=Decimal('1500.00'),
            created_at=datetime.now(timezone.utc)
        )
        
        contract = ContractResult(
            id=str(uuid.uuid4()),
            search_id=search_request.id,
            reestr_number=str(uuid.uuid4())[:8],
            contract_url="http://example.com",
            sign_date=datetime.now(timezone.utc),
            unit_price=unit_price,
            match_type="exact",
            ai_score=85,
            manufacturer_target="Test Manufacturer",
            manufacturer_found="Found Manufacturer",
            raw_data_json={"test": "data"}
        )
        
        # Set the relationship
        contract.search_request = search_request
        
        return contract


class TestExcelReportGeneration:
    """Test Excel report generation functionality."""
    
    def test_generate_excel_report_success(self):
        """Test successful Excel report generation."""
        # Create dummy contracts
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
            self._create_dummy_contract(unit_price=Decimal('2000.00')),
            self._create_dummy_contract(unit_price=Decimal('3000.00')),
        ]
        
        search_id = str(uuid.uuid4())
        
        # Create temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate report
            filepath = generate_excel_report(search_id, contracts, output_dir=temp_dir)
            
            # Verify file was created
            assert os.path.exists(filepath)
            assert filepath.endswith('.xlsx')
            assert search_id in filepath
            
            # Verify file size (should not be empty)
            assert os.path.getsize(filepath) > 0
            
            # Verify file can be read with pandas
            import pandas as pd
            excel_data = pd.read_excel(filepath, sheet_name=None)
            
            # Should have both sheets
            assert 'Сводка' in excel_data
            assert 'Детали' in excel_data
            
            # Verify summary sheet has correct data
            summary_df = excel_data['Сводка']
            assert len(summary_df) == 7  # 7 summary rows
            assert summary_df.iloc[0, 1] == search_id  # Search ID in second column
            
            # Verify details sheet has correct number of rows
            details_df = excel_data['Детали']
            assert len(details_df) == 3  # 3 contracts
    
    def test_generate_excel_report_with_no_prices(self):
        """Test Excel report generation when contracts have no prices."""
        contracts = [
            self._create_dummy_contract(unit_price=None),
            self._create_dummy_contract(unit_price=None),
        ]
        
        search_id = str(uuid.uuid4())
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = generate_excel_report(search_id, contracts, output_dir=temp_dir)
            
            assert os.path.exists(filepath)
            
            # Verify file can be read
            import pandas as pd
            excel_data = pd.read_excel(filepath, sheet_name=None)
            
            # Details sheet should be empty (no contracts with prices)
            details_df = excel_data['Детали']
            assert len(details_df) == 0
    
    def test_generate_excel_report_with_empty_contracts(self):
        """Test Excel report generation with empty contracts list."""
        search_id = str(uuid.uuid4())
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="Cannot generate report: contracts list is empty"):
                generate_excel_report(search_id, [], output_dir=temp_dir)
    
    def test_generate_excel_report_creates_directory(self):
        """Test that report generation creates output directory if it doesn't exist."""
        contracts = [
            self._create_dummy_contract(unit_price=Decimal('1000.00')),
        ]
        
        search_id = str(uuid.uuid4())
        temp_dir = tempfile.mkdtemp()
        non_existent_dir = os.path.join(temp_dir, "subdir", "reports")
        
        try:
            # Directory shouldn't exist yet
            assert not os.path.exists(non_existent_dir)
            
            # Generate report - should create directory
            filepath = generate_excel_report(search_id, contracts, output_dir=non_existent_dir)
            
            # Directory should now exist
            assert os.path.exists(non_existent_dir)
            assert os.path.exists(filepath)
        finally:
            # Cleanup
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _create_dummy_contract(self, unit_price=None):
        """Helper to create a dummy ContractResult object."""
        search_request = SearchRequest(
            id=str(uuid.uuid4()),
            input_source="test",
            object_name="Test Object",
            status=SearchStatus.COMPLETED,
            found_total=5,
            processed_count=5,
            nmc_value=Decimal('1500.00'),
            created_at=datetime.now(timezone.utc)
        )
        
        contract = ContractResult(
            id=str(uuid.uuid4()),
            search_id=search_request.id,
            reestr_number=str(uuid.uuid4())[:8],
            contract_url="http://example.com",
            sign_date=datetime.now(timezone.utc),
            unit_price=unit_price,
            match_type="exact",
            ai_score=85,
            manufacturer_target="Test Manufacturer",
            manufacturer_found="Found Manufacturer",
            raw_data_json={"test": "data"}
        )
        
        # Set the relationship
        contract.search_request = search_request
        
        return contract


if __name__ == "__main__":
    pytest.main([__file__, "-v"])