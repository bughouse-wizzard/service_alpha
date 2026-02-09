import uuid
from datetime import datetime, date
from decimal import Decimal
import json

def test_search_request_creation(session):
    """Test creating a SearchRequest model."""
    from app.models import SearchRequest, SearchStatus
    
    # Create a search request
    search_request = SearchRequest(
        object_name="Test Object",
        ktru="123456",
        okpd2="45.11.10",
        okved2="45.11",
        region="Moscow",
        price_min=Decimal("1000.00"),
        price_max=Decimal("5000.00"),
        date_from=date(2024, 1, 1),
        date_to=date(2024, 12, 31),
        nmc_value=Decimal("3000.00"),
        status=SearchStatus.RUNNING
    )
    
    session.add(search_request)
    session.commit()
    
    # Verify the search request was created
    assert search_request.id is not None
    assert search_request.object_name == "Test Object"
    assert search_request.ktru == "123456"
    assert search_request.okpd2 == "45.11.10"
    assert search_request.okved2 == "45.11"
    assert search_request.region == "Moscow"
    assert search_request.price_min == Decimal("1000.00")
    assert search_request.price_max == Decimal("5000.00")
    assert search_request.date_from == date(2024, 1, 1)
    assert search_request.date_to == date(2024, 12, 31)
    assert search_request.nmc_value == Decimal("3000.00")
    assert search_request.status == SearchStatus.RUNNING
    assert search_request.created_at is not None
    assert search_request.updated_at is not None
    
    # Test to_dict method
    search_dict = search_request.to_dict()
    assert search_dict['id'] == str(search_request.id)
    assert search_dict['status'] == 'RUNNING'
    assert search_dict['object_name'] == 'Test Object'
    assert search_dict['nmc_value'] == 3000.00

def test_contract_result_creation(session):
    """Test creating a ContractResult model."""
    from app.models import SearchRequest, SearchStatus, ContractResult, MatchType
    
    # First create a search request
    search_request = SearchRequest(
        object_name="Test Object",
        status=SearchStatus.RUNNING
    )
    session.add(search_request)
    session.commit()
    
    # Create a contract result
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="1234567890",
        price=Decimal("2500.50"),
        match_type=MatchType.EXACT,
        ai_score=Decimal("0.95"),
        supplier_name="Test Supplier Inc.",
        contract_date=date(2024, 6, 15),
        delivery_date=date(2024, 7, 15),
        raw_data_json={"contract_id": "12345", "supplier": "Test Supplier"}
    )
    
    session.add(contract_result)
    session.commit()
    
    # Verify the contract result was created
    assert contract_result.id is not None
    assert contract_result.search_id == search_request.id
    assert contract_result.reestr_number == "1234567890"
    assert contract_result.price == Decimal("2500.50")
    assert contract_result.match_type == MatchType.EXACT
    assert contract_result.ai_score == Decimal("0.95")
    assert contract_result.supplier_name == "Test Supplier Inc."
    assert contract_result.contract_date == date(2024, 6, 15)
    assert contract_result.delivery_date == date(2024, 7, 15)
    assert contract_result.raw_data_json == {"contract_id": "12345", "supplier": "Test Supplier"}
    
    # Test relationship
    assert contract_result.search_request == search_request
    assert len(search_request.contract_results) == 1
    assert search_request.contract_results[0] == contract_result
    
    # Test to_dict method
    contract_dict = contract_result.to_dict()
    assert contract_dict['id'] == str(contract_result.id)
    assert contract_dict['search_id'] == str(search_request.id)
    assert contract_dict['reestr_number'] == '1234567890'
    assert contract_dict['price'] == 2500.50
    assert contract_dict['match_type'] == 'EXACT'
    assert contract_dict['ai_score'] == 0.95

def test_spec_comparison_row_creation(session):
    """Test creating a SpecComparisonRow model."""
    from app.models import SearchRequest, SearchStatus, ContractResult, MatchType, SpecComparisonRow, MatchStatus
    
    # Create search request and contract result
    search_request = SearchRequest(
        object_name="Test Object",
        status=SearchStatus.RUNNING
    )
    session.add(search_request)
    session.commit()
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="1234567890",
        price=Decimal("2500.50"),
        match_type=MatchType.EXACT
    )
    session.add(contract_result)
    session.commit()
    
    # Create a spec comparison row
    spec_row = SpecComparisonRow(
        contract_result_id=contract_result.id,
        parameter_name="Material",
        target_value="Steel",
        actual_value="Stainless Steel",
        match_status=MatchStatus.PARTIAL_MATCH,
        unit_of_measure="kg",
        importance_weight=Decimal("0.8")
    )
    
    session.add(spec_row)
    session.commit()
    
    # Verify the spec comparison row was created
    assert spec_row.id is not None
    assert spec_row.contract_result_id == contract_result.id
    assert spec_row.parameter_name == "Material"
    assert spec_row.target_value == "Steel"
    assert spec_row.actual_value == "Stainless Steel"
    assert spec_row.match_status == MatchStatus.PARTIAL_MATCH
    assert spec_row.unit_of_measure == "kg"
    assert spec_row.importance_weight == Decimal("0.8")
    
    # Test relationship
    assert spec_row.contract_result == contract_result
    assert len(contract_result.spec_comparisons) == 1
    assert contract_result.spec_comparisons[0] == spec_row
    
    # Test to_dict method
    spec_dict = spec_row.to_dict()
    assert spec_dict['id'] == str(spec_row.id)
    assert spec_dict['contract_result_id'] == str(contract_result.id)
    assert spec_dict['parameter_name'] == 'Material'
    assert spec_dict['target_value'] == 'Steel'
    assert spec_dict['actual_value'] == 'Stainless Steel'
    assert spec_dict['match_status'] == 'PARTIAL_MATCH'
    assert spec_dict['unit_of_measure'] == 'kg'
    assert spec_dict['importance_weight'] == 0.8

def test_cascade_deletion(session):
    """Test cascade deletion of related records."""
    from app.models import SearchRequest, SearchStatus, ContractResult, MatchType, SpecComparisonRow, MatchStatus
    
    # Create a hierarchy: SearchRequest -> ContractResult -> SpecComparisonRow
    search_request = SearchRequest(
        object_name="Test Object",
        status=SearchStatus.RUNNING
    )
    session.add(search_request)
    session.commit()
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="1234567890",
        price=Decimal("2500.50"),
        match_type=MatchType.EXACT
    )
    session.add(contract_result)
    session.commit()
    
    spec_row = SpecComparisonRow(
        contract_result_id=contract_result.id,
        parameter_name="Material",
        target_value="Steel",
        actual_value="Stainless Steel",
        match_status=MatchStatus.PARTIAL_MATCH
    )
    session.add(spec_row)
    session.commit()
    
    # Get fresh counts for just our test records
    search_count = session.query(SearchRequest).filter_by(id=search_request.id).count()
    contract_count = session.query(ContractResult).filter_by(search_id=search_request.id).count()
    spec_count = session.query(SpecComparisonRow).filter_by(contract_result_id=contract_result.id).count()
    
    # Verify all records exist
    assert search_count == 1
    assert contract_count == 1
    assert spec_count == 1
    
    # Delete the search request (should cascade)
    session.delete(search_request)
    session.commit()
    
    # Verify all related records were deleted
    assert session.query(SearchRequest).filter_by(id=search_request.id).count() == 0
    assert session.query(ContractResult).filter_by(search_id=search_request.id).count() == 0
    assert session.query(SpecComparisonRow).filter_by(contract_result_id=contract_result.id).count() == 0

def test_indexes_exist(session):
    """Verify that indexes are properly created."""
    from sqlalchemy import inspect
    
    inspector = inspect(session.bind)
    
    # Check indexes on search_requests table
    search_request_indexes = inspector.get_indexes('search_requests')
    status_index = any(idx['name'] == 'ix_search_requests_status' for idx in search_request_indexes)
    assert status_index, "Index on search_requests.status should exist"
    
    # Check indexes on contract_results table
    contract_result_indexes = inspector.get_indexes('contract_results')
    search_id_index = any(idx['name'] == 'ix_contract_results_search_id' for idx in contract_result_indexes)
    reestr_number_index = any(idx['name'] == 'ix_contract_results_reestr_number' for idx in contract_result_indexes)
    
    assert search_id_index, "Index on contract_results.search_id should exist"
    assert reestr_number_index, "Index on contract_results.reestr_number should exist"
    
    # Check indexes on spec_comparison_rows table
    spec_row_indexes = inspector.get_indexes('spec_comparison_rows')
    contract_result_id_index = any(idx['name'] == 'ix_spec_comparison_rows_contract_result_id' for idx in spec_row_indexes)
    assert contract_result_id_index, "Index on spec_comparison_rows.contract_result_id should exist"