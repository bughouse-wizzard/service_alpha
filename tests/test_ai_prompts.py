"""
Tests for AI prompts module.
"""

import pytest
from app.services.ai.prompts import (
    extract_specs_from_tz,
    extract_specs_from_contract,
    compare_specs,
    MatchType,
    AIClientWrapper
)


def test_extract_specs_from_tz_returns_list():
    """Test that extract_specs_from_tz returns a list."""
    # Arrange
    dummy_text = "Мощность: 100 кВт, напряжение 220 В"
    
    # Act
    result = extract_specs_from_tz(dummy_text)
    
    # Assert
    assert isinstance(result, list)
    assert len(result) > 0
    for spec in result:
        assert "name" in spec
        assert "value" in spec
        assert "is_mandatory" in spec


def test_extract_specs_from_tz_has_required_keys():
    """Test that extracted specs have required keys."""
    # Arrange
    dummy_text = "Технические требования: мощность 100 кВт"
    
    # Act
    result = extract_specs_from_tz(dummy_text)
    
    # Assert
    for spec in result:
        required_keys = ["name", "value", "is_mandatory"]
        for key in required_keys:
            assert key in spec


def test_extract_specs_from_contract_returns_dict():
    """Test that extract_specs_from_contract returns a dict with required keys."""
    # Arrange
    dummy_text = "Контракт на поставку оборудования. Производитель: ООО ТехноПром"
    
    # Act
    result = extract_specs_from_contract(dummy_text)
    
    # Assert
    assert isinstance(result, dict)
    assert "specs" in result
    assert "manufacturer" in result
    assert isinstance(result["specs"], list)
    assert isinstance(result["manufacturer"], str)


def test_extract_specs_from_contract_specs_have_required_keys():
    """Test that specs in contract extraction have required keys."""
    # Arrange
    dummy_text = "Оборудование: мощность 95 кВт"
    
    # Act
    result = extract_specs_from_contract(dummy_text)
    
    # Assert
    for spec in result["specs"]:
        required_keys = ["name", "value", "source"]
        for key in required_keys:
            assert key in spec


def test_compare_specs_returns_correct_structure():
    """Test that compare_specs returns dict with score and match_type."""
    # Arrange
    target_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "is_mandatory": True},
        {"name": "напряжение", "value": 220, "unit": "В", "is_mandatory": True}
    ]
    
    actual_specs = [
        {"name": "мощность", "value": 95, "unit": "кВт", "source": "contract"},
        {"name": "напряжение", "value": 230, "unit": "В", "source": "contract"}
    ]
    
    # Act
    result = compare_specs(target_specs, actual_specs)
    
    # Assert
    assert isinstance(result, dict)
    assert "score" in result
    assert "match_type" in result
    assert "diff_log" in result
    assert "matches" in result
    assert "total" in result
    
    # Check types
    assert isinstance(result["score"], int)
    assert isinstance(result["match_type"], MatchType)
    assert isinstance(result["diff_log"], list)
    assert isinstance(result["matches"], int)
    assert isinstance(result["total"], int)
    
    # Check value ranges
    assert 0 <= result["score"] <= 100
    assert result["matches"] <= result["total"]


def test_compare_specs_score_and_match_type_present():
    """Test that score and match_type keys are present in compare_specs result."""
    # Arrange
    target_specs = [
        {"name": "температура", "value": 25, "unit": "°C", "is_mandatory": False}
    ]
    
    actual_specs = [
        {"name": "температура", "value": 25, "unit": "°C", "source": "contract"}
    ]
    
    # Act
    result = compare_specs(target_specs, actual_specs)
    
    # Assert
    assert "score" in result
    assert "match_type" in result
    assert result["score"] >= 0
    assert result["match_type"] in [MatchType.EXACT, MatchType.PARTIAL, 
                                   MatchType.SIMILAR, MatchType.NO_MATCH]


def test_compare_specs_exact_match():
    """Test exact match scenario."""
    # Arrange
    target_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "is_mandatory": True},
        {"name": "напряжение", "value": 220, "unit": "В", "is_mandatory": True}
    ]
    
    actual_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "source": "contract"},
        {"name": "напряжение", "value": 220, "unit": "В", "source": "contract"}
    ]
    
    # Act
    result = compare_specs(target_specs, actual_specs)
    
    # Assert
    assert result["score"] == 100
    assert result["match_type"] == MatchType.EXACT
    assert result["matches"] == 2
    assert result["total"] == 2


def test_compare_specs_partial_match():
    """Test partial match scenario."""
    # Arrange
    target_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "is_mandatory": True},
        {"name": "напряжение", "value": 220, "unit": "В", "is_mandatory": True},
        {"name": "вес", "value": 50, "unit": "кг", "is_mandatory": False}
    ]
    
    actual_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "source": "contract"},
        {"name": "напряжение", "value": 230, "unit": "В", "source": "contract"}
    ]
    
    # Act
    result = compare_specs(target_specs, actual_specs)
    
    # Assert
    assert 0 <= result["score"] <= 100
    assert result["total"] == 3


def test_compare_specs_no_match():
    """Test no match scenario."""
    # Arrange
    target_specs = [
        {"name": "мощность", "value": 100, "unit": "кВт", "is_mandatory": True}
    ]
    
    actual_specs = [
        {"name": "температура", "value": 25, "unit": "°C", "source": "contract"}
    ]
    
    # Act
    result = compare_specs(target_specs, actual_specs)
    
    # Assert
    assert result["score"] == 0
    assert result["match_type"] == MatchType.NO_MATCH
    assert result["matches"] == 0


def test_ai_client_wrapper_integration():
    """Test AIClientWrapper integration."""
    # Arrange
    client = AIClientWrapper()
    dummy_text = "Мощность 100 кВт"
    
    # Act & Assert - Test that methods exist and return expected types
    # Note: These are async methods in the wrapper, but we're testing structure
    assert hasattr(client, 'extract_specs_from_tz')
    assert hasattr(client, 'extract_specs_from_contract')
    assert hasattr(client, 'compare_specs')


def test_empty_input_handling():
    """Test handling of empty input strings."""
    # Arrange
    empty_text = ""
    
    # Act
    tz_result = extract_specs_from_tz(empty_text)
    contract_result = extract_specs_from_contract(empty_text)
    
    # Assert
    assert isinstance(tz_result, list)
    assert isinstance(contract_result, dict)
    assert "specs" in contract_result
    assert "manufacturer" in contract_result


def test_special_characters_in_text():
    """Test handling of text with special characters."""
    # Arrange
    special_text = "Мощность: 100±5% кВт, напряжение ~220 В"
    
    # Act
    tz_result = extract_specs_from_tz(special_text)
    
    # Assert
    assert isinstance(tz_result, list)
    # Should not crash with special characters


if __name__ == "__main__":
    pytest.main([__file__, "-v"])