import pytest
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.search_request import SearchRequest, SearchStatus
from app.models.contract_result import ContractResult
from app.models.spec_comparison_row import SpecComparisonRow, MatchStatus


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)


def test_create_search_request(db_session):
    """Test creating a SearchRequest with all required fields."""
    # Create a search request
    search_request = SearchRequest(
        object_name="Test Object",
        ktru="123456",
        okpd2="10.11.12",
        okved2="45.20",
        region="Moscow",
        customer_name="Test Customer",
        customer_inn="1234567890",
        price_from=1000.0,
        price_to=5000.0,
        date_from=datetime(2024, 1, 1),
        date_to=datetime(2024, 12, 31),
        nmc_value=3000.0,
        status=SearchStatus.RUNNING,
        search_parameters={"additional_param": "value"},
        error_message=None
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    # Assertions
    assert search_request.id is not None
    assert search_request.object_name == "Test Object"
    assert search_request.ktru == "123456"
    assert search_request.okpd2 == "10.11.12"
    assert search_request.status == SearchStatus.RUNNING
    assert search_request.nmc_value == 3000.0
    assert search_request.created_at is not None
    assert search_request.updated_at is not None
    
    # Test retrieving the search request
    retrieved = db_session.query(SearchRequest).filter_by(id=search_request.id).first()
    assert retrieved is not None
    assert retrieved.id == search_request.id
    assert retrieved.object_name == "Test Object"


def test_search_request_status_enum(db_session):
    """Test all possible status values for SearchRequest."""
    # Test each status
    for status in SearchStatus:
        search_request = SearchRequest(
            object_name=f"Test Object - {status.value}",
            status=status
        )
        
        db_session.add(search_request)
        db_session.commit()
        db_session.refresh(search_request)
        
        assert search_request.status == status
        
        # Clean up for next iteration
        db_session.delete(search_request)
        db_session.commit()


def test_create_contract_result_with_foreign_key(db_session):
    """Test creating a ContractResult with foreign key to SearchRequest."""
    # First create a search request
    search_request = SearchRequest(
        object_name="Parent Search Request",
        status=SearchStatus.DONE
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    # Create a contract result linked to the search request
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="CONTRACT-001",
        price=15000.0,
        match_type="EXACT",
        ai_score=0.95,
        raw_data_json={"source": "external_api", "data": {"field": "value"}},
        contract_date=datetime(2024, 6, 15),
        supplier_name="Test Supplier",
        supplier_inn="0987654321",
        contract_status="ACTIVE"
    )
    
    db_session.add(contract_result)
    db_session.commit()
    db_session.refresh(contract_result)
    
    # Assertions
    assert contract_result.id is not None
    assert contract_result.search_id == search_request.id
    assert contract_result.reestr_number == "CONTRACT-001"
    assert contract_result.price == 15000.0
    assert contract_result.match_type == "EXACT"
    assert contract_result.ai_score == 0.95
    assert contract_result.raw_data_json == {"source": "external_api", "data": {"field": "value"}}
    assert contract_result.supplier_name == "Test Supplier"
    
    # Test relationship
    assert contract_result.search_request.id == search_request.id
    assert contract_result.search_request.object_name == "Parent Search Request"
    
    # Test back relationship
    assert len(search_request.contract_results) == 1
    assert search_request.contract_results[0].id == contract_result.id


def test_create_spec_comparison_row(db_session):
    """Test creating a SpecComparisonRow with foreign key to ContractResult."""
    # Create parent objects
    search_request = SearchRequest(
        object_name="Parent Search",
        status=SearchStatus.DONE
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="CONTRACT-002",
        price=20000.0
    )
    
    db_session.add(contract_result)
    db_session.commit()
    db_session.refresh(contract_result)
    
    # Create spec comparison row
    spec_row = SpecComparisonRow(
        contract_result_id=contract_result.id,
        target_value="100 units",
        actual_value="100 units",
        match_status=MatchStatus.MATCH,
        parameter_name="quantity",
        parameter_unit="units",
        confidence_score=1.0
    )
    
    db_session.add(spec_row)
    db_session.commit()
    db_session.refresh(spec_row)
    
    # Assertions
    assert spec_row.id is not None
    assert spec_row.contract_result_id == contract_result.id
    assert spec_row.target_value == "100 units"
    assert spec_row.actual_value == "100 units"
    assert spec_row.match_status == MatchStatus.MATCH
    assert spec_row.parameter_name == "quantity"
    assert spec_row.confidence_score == 1.0
    
    # Test relationships
    assert spec_row.contract_result.id == contract_result.id
    assert len(contract_result.spec_comparisons) == 1
    assert contract_result.spec_comparisons[0].id == spec_row.id


def test_cascade_deletes(db_session):
    """Test that cascade deletes work correctly."""
    # Create hierarchy: SearchRequest -> ContractResult -> SpecComparisonRow
    search_request = SearchRequest(
        object_name="Cascade Test",
        status=SearchStatus.DONE
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="CASCADE-001",
        price=1000.0
    )
    
    db_session.add(contract_result)
    db_session.commit()
    db_session.refresh(contract_result)
    
    spec_row = SpecComparisonRow(
        contract_result_id=contract_result.id,
        target_value="test",
        actual_value="test",
        match_status=MatchStatus.MATCH,
        parameter_name="test_param"
    )
    
    db_session.add(spec_row)
    db_session.commit()
    
    # Verify all objects exist
    assert db_session.query(SearchRequest).count() == 1
    assert db_session.query(ContractResult).count() == 1
    assert db_session.query(SpecComparisonRow).count() == 1
    
    # Delete search request (should cascade)
    db_session.delete(search_request)
    db_session.commit()
    
    # Verify all related objects are deleted
    assert db_session.query(SearchRequest).count() == 0
    assert db_session.query(ContractResult).count() == 0
    assert db_session.query(SpecComparisonRow).count() == 0


def test_indexes_exist(db_session):
    """Verify that required indexes exist by checking query performance."""
    # Create test data
    search_request = SearchRequest(
        object_name="Index Test",
        status=SearchStatus.DONE
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    # Create multiple contract results with different reestr numbers
    for i in range(3):
        contract_result = ContractResult(
            search_id=search_request.id,
            reestr_number=f"INDEX-TEST-{i:03d}",
            price=1000.0 * (i + 1),
            ai_score=0.1 * (i + 1)
        )
        db_session.add(contract_result)
    
    db_session.commit()
    
    # Test query using indexed field (reestr_number)
    result = db_session.query(ContractResult).filter_by(
        reestr_number="INDEX-TEST-001"
    ).first()
    
    assert result is not None
    assert result.reestr_number == "INDEX-TEST-001"
    
    # Test query using another indexed field (search_id)
    results = db_session.query(ContractResult).filter_by(
        search_id=search_request.id
    ).all()
    
    assert len(results) == 3
    
    # Test query using price index
    results = db_session.query(ContractResult).filter(
        ContractResult.price > 1500.0
    ).all()
    
    assert len(results) == 2  # Prices 2000 and 3000


def test_json_field_operations(db_session):
    """Test JSON field operations in ContractResult."""
    search_request = SearchRequest(
        object_name="JSON Test",
        status=SearchStatus.DONE
    )
    
    db_session.add(search_request)
    db_session.commit()
    db_session.refresh(search_request)
    
    # Create contract result with complex JSON data
    complex_json = {
        "source": "external_api",
        "timestamp": "2024-01-15T10:30:00Z",
        "metadata": {
            "version": "1.0",
            "provider": "data_provider"
        },
        "items": [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"}
        ]
    }
    
    contract_result = ContractResult(
        search_id=search_request.id,
        reestr_number="JSON-TEST-001",
        price=5000.0,
        raw_data_json=complex_json
    )
    
    db_session.add(contract_result)
    db_session.commit()
    db_session.refresh(contract_result)
    
    # Assert JSON data is stored and retrieved correctly
    assert contract_result.raw_data_json == complex_json
    assert contract_result.raw_data_json["source"] == "external_api"
    assert contract_result.raw_data_json["metadata"]["provider"] == "data_provider"
    assert len(contract_result.raw_data_json["items"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])