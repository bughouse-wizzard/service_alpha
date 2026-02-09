import pytest
import uuid
import json
from datetime import datetime
from app.models.search_request import SearchRequest, SearchStatus
from app.models.contract_result import ContractResult, MatchType
from app.models.spec_comparison_row import SpecComparisonRow, MatchStatus


def test_search_request_creation(database):
    """Test creating a SearchRequest"""
    # Create a search request
    search_request = SearchRequest(
        object_name="Test Object",
        ktru="123456",
        okpd2="01.11.11",
        okved2="01.11",
        region="Moscow",
        customer_name="Test Customer",
        customer_inn="1234567890",
        price_from=1000.0,
        price_to=5000.0,
        publication_date_from=datetime(2024, 1, 1),
        publication_date_to=datetime(2024, 12, 31),
        additional_filters="test filters",
        nmc_value=3000.0,
        status=SearchStatus.RUNNING
    )
    
    # Add to database
    database.session.add(search_request)
    database.session.commit()
    
    # Verify the search request was saved
    assert search_request.id is not None
    assert search_request.object_name == "Test Object"
    assert search_request.status == SearchStatus.RUNNING
    assert search_request.nmc_value == 3000.0
    
    # Test to_dict method
    search_dict = search_request.to_dict()
    assert search_dict['object_name'] == "Test Object"
    assert search_dict['status'] == "RUNNING"
    assert search_dict['nmc_value'] == 3000.0
    
    # Cleanup
    database.session.delete(search_request)
    database.session.commit()


def test_contract_result_creation(database):
    """Test creating a ContractResult linked to SearchRequest"""
    # First create a search request
    search_request = SearchRequest(
        object_name="Test Object for Contract",
        status=SearchStatus.DONE
    )
    database.session.add(search_request)
    database.session.commit()
    
    # Create contract result data
    raw_data = {
        "contract_number": "12345",
        "supplier": "Test Supplier",
        "details": {"key": "value"}
    }
    
    # Create a contract result
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="REESTR-2024-001",
        price=2500.0,
        match_type=MatchType.EXACT,
        ai_score=0.95,
        raw_data_json=raw_data,
        contract_date=datetime(2024, 6, 15),
        supplier_name="Test Supplier Inc.",
        supplier_inn="0987654321"
    )
    
    # Add to database
    database.session.add(contract_result)
    database.session.commit()
    
    # Verify the contract result was saved
    assert contract_result.id is not None
    assert contract_result.reestr_number == "REESTR-2024-001"
    assert contract_result.price == 2500.0
    assert contract_result.match_type == MatchType.EXACT
    assert contract_result.ai_score == 0.95
    assert contract_result.raw_data_json == raw_data
    assert contract_result.search_request.id == search_request.id
    
    # Test to_dict method
    contract_dict = contract_result.to_dict()
    assert contract_dict['reestr_number'] == "REESTR-2024-001"
    assert contract_dict['match_type'] == "EXACT"
    assert contract_dict['ai_score'] == 0.95
    assert contract_dict['raw_data_json'] == raw_data
    
    # Cleanup
    database.session.delete(contract_result)
    database.session.delete(search_request)
    database.session.commit()


def test_spec_comparison_row_creation(database):
    """Test creating a SpecComparisonRow linked to ContractResult"""
    # Create search request
    search_request = SearchRequest(
        object_name="Test Object for Spec",
        status=SearchStatus.DONE
    )
    database.session.add(search_request)
    database.session.commit()
    
    # Create contract result
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="REESTR-2024-002",
        price=3500.0,
        match_type=MatchType.PARTIAL,
        ai_score=0.75,
        raw_data_json={"test": "data"}
    )
    database.session.add(contract_result)
    database.session.commit()
    
    # Create spec comparison row
    spec_row = SpecComparisonRow(
        contract_result_id=contract_result.id,
        parameter_name="Material",
        target_value="Steel",
        actual_value="Stainless Steel",
        match_status=MatchStatus.PARTIAL_MATCH,
        unit_of_measure="kg",
        importance_weight=0.8,
        confidence_score=0.9
    )
    
    # Add to database
    database.session.add(spec_row)
    database.session.commit()
    
    # Verify the spec row was saved
    assert spec_row.id is not None
    assert spec_row.parameter_name == "Material"
    assert spec_row.target_value == "Steel"
    assert spec_row.actual_value == "Stainless Steel"
    assert spec_row.match_status == MatchStatus.PARTIAL_MATCH
    assert spec_row.unit_of_measure == "kg"
    assert spec_row.importance_weight == 0.8
    assert spec_row.confidence_score == 0.9
    assert spec_row.contract_result.id == contract_result.id
    
    # Test to_dict method
    spec_dict = spec_row.to_dict()
    assert spec_dict['parameter_name'] == "Material"
    assert spec_dict['target_value'] == "Steel"
    assert spec_dict['actual_value'] == "Stainless Steel"
    assert spec_dict['match_status'] == "PARTIAL_MATCH"
    
    # Cleanup
    database.session.delete(spec_row)
    database.session.delete(contract_result)
    database.session.delete(search_request)
    database.session.commit()


def test_relationships(database):
    """Test relationships between models"""
    # Create search request
    search_request = SearchRequest(
        object_name="Relationship Test",
        status=SearchStatus.DONE
    )
    database.session.add(search_request)
    database.session.commit()
    
    # Create multiple contract results
    contract1 = ContractResult(
        search_id=search_request.id,
        reestr_number="REESTR-001",
        price=1000.0,
        match_type=MatchType.EXACT,
        ai_score=0.95,
        raw_data_json={"data": "1"}
    )
    
    contract2 = ContractResult(
        search_id=search_request.id,
        reestr_number="REESTR-002",
        price=2000.0,
        match_type=MatchType.PARTIAL,
        ai_score=0.85,
        raw_data_json={"data": "2"}
    )
    
    database.session.add_all([contract1, contract2])
    database.session.commit()
    
    # Create spec rows for contract1
    spec1 = SpecComparisonRow(
        contract_result_id=contract1.id,
        parameter_name="Param1",
        target_value="Target1",
        actual_value="Actual1",
        match_status=MatchStatus.MATCH
    )
    
    spec2 = SpecComparisonRow(
        contract_result_id=contract1.id,
        parameter_name="Param2",
        target_value="Target2",
        actual_value="Actual2",
        match_status=MatchStatus.NO_MATCH
    )
    
    database.session.add_all([spec1, spec2])
    database.session.commit()
    
    # Test relationships
    assert len(search_request.contract_results) == 2
    assert contract1 in search_request.contract_results
    assert contract2 in search_request.contract_results
    
    assert len(contract1.spec_comparison_rows) == 2
    assert spec1 in contract1.spec_comparison_rows
    assert spec2 in contract1.spec_comparison_rows
    
    # Test cascade delete
    database.session.delete(search_request)
    database.session.commit()
    
    # Verify all related records were deleted
    remaining_contracts = ContractResult.query.all()
    remaining_specs = SpecComparisonRow.query.all()
    
    assert len(remaining_contracts) == 0
    assert len(remaining_specs) == 0


def test_enum_values():
    """Test enum values are correct"""
    # SearchStatus enum
    assert SearchStatus.RUNNING.value == "RUNNING"
    assert SearchStatus.DONE.value == "DONE"
    assert SearchStatus.STOPPED.value == "STOPPED"
    assert SearchStatus.ERROR.value == "ERROR"
    
    # MatchType enum
    assert MatchType.EXACT.value == "EXACT"
    assert MatchType.PARTIAL.value == "PARTIAL"
    assert MatchType.SIMILAR.value == "SIMILAR"
    assert MatchType.NO_MATCH.value == "NO_MATCH"
    
    # MatchStatus enum
    assert MatchStatus.MATCH.value == "MATCH"
    assert MatchStatus.PARTIAL_MATCH.value == "PARTIAL_MATCH"
    assert MatchStatus.NO_MATCH.value == "NO_MATCH"
    assert MatchStatus.NOT_SPECIFIED.value == "NOT_SPECIFIED"


def test_indexes(database):
    """Test that indexes are working"""
    # Create test data
    search_request = SearchRequest(
        object_name="Index Test",
        status=SearchStatus.RUNNING
    )
    database.session.add(search_request)
    database.session.commit()
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="INDEX-TEST-001",
        price=1000.0,
        match_type=MatchType.EXACT,
        ai_score=0.9,
        raw_data_json={"test": "index"}
    )
    database.session.add(contract_result)
    database.session.commit()
    
    # Query using indexed fields should work
    contracts_by_search = ContractResult.query.filter_by(search_id=search_request.id).all()
    assert len(contracts_by_search) == 1
    assert contracts_by_search[0].reestr_number == "INDEX-TEST-001"
    
    # Cleanup
    database.session.delete(contract_result)
    database.session.delete(search_request)
    database.session.commit()