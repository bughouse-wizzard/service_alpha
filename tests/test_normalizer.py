"""
Tests for the specification normalizer.
"""

import pytest
from app.services.matcher.normalizer import (
    to_lowercase,
    normalize_units,
    extract_numeric_value,
    handle_range,
    normalize_specification
)


def test_to_lowercase():
    """Test lowercase conversion."""
    assert to_lowercase("Hello World") == "hello world"
    assert to_lowercase("TEST") == "test"
    assert to_lowercase("Mixed CASE 123") == "mixed case 123"
    assert to_lowercase("") == ""


def test_normalize_units():
    """Test unit normalization."""
    # Weight units
    assert normalize_units("10 кг") == "10 kg"
    assert normalize_units("500 грамм") == "500 g"
    assert normalize_units("2 kilogram") == "2 kg"
    
    # Volume units
    assert normalize_units("1 литр") == "1 l"
    assert normalize_units("250 миллилитр") == "250 ml"
    
    # Length units
    assert normalize_units("5 метр") == "5 m"
    assert normalize_units("30 сантиметр") == "30 cm"
    
    # Currency units
    assert normalize_units("100 руб") == "100 rub"
    assert normalize_units("50 рублей") == "50 rub"
    assert normalize_units("25 USD") == "25 usd"
    assert normalize_units("30 €") == "30 eur"
    
    # Area units
    assert normalize_units("80 м2") == "80 m2"
    assert normalize_units("100 кв.м") == "100 m2"
    assert normalize_units("50 квадратный метр") == "50 m2"
    
    # Mixed cases
    assert normalize_units("10 КГ 20 Г") == "10 kg 20 g"
    assert normalize_units("5л 250мл") == "5l 250ml"


def test_extract_numeric_value():
    """Test numeric value extraction."""
    # Test case 1: '100.50 RUB'
    result1 = extract_numeric_value("100.50 RUB")
    assert result1 is not None
    assert result1['value'] == 100.5
    assert result1['unit'] == 'rub'
    
    # Test case 2: '80 g/m2'
    result2 = extract_numeric_value("80 g/m2")
    assert result2 is not None
    assert result2['value'] == 80.0
    assert result2['unit'] == 'g/m2'
    
    # Test case 3: 'class A' (no numeric value)
    result3 = extract_numeric_value("class A")
    assert result3 is None
    
    # Additional test cases
    result4 = extract_numeric_value("approx 500 ml")
    assert result4 is not None
    assert result4['value'] == 500.0
    assert result4['unit'] == 'ml'
    
    result5 = extract_numeric_value("about 2.5 kg")
    assert result5 is not None
    assert result5['value'] == 2.5
    assert result5['unit'] == 'kg'
    
    result6 = extract_numeric_value("~100 рублей")
    assert result6 is not None
    assert result6['value'] == 100.0
    assert result6['unit'] == 'rub'
    
    # Test with negative numbers
    result7 = extract_numeric_value("-15.5°C")
    assert result7 is not None
    assert result7['value'] == -15.5
    assert result7['unit'] == '°c'
    
    # Test with unit before number
    result8 = extract_numeric_value("USD 25")
    assert result8 is not None
    assert result8['value'] == 25.0
    assert result8['unit'] == 'usd'


def test_handle_range():
    """Test range handling."""
    # Simple dash range
    result1 = handle_range("10-20")
    assert result1 is not None
    assert result1['min'] == 10.0
    assert result1['max'] == 20.0
    
    # Range with spaces
    result2 = handle_range("5 - 15")
    assert result2 is not None
    assert result2['min'] == 5.0
    assert result2['max'] == 15.0
    
    # Range with 'to'
    result3 = handle_range("100 to 200")
    assert result3 is not None
    assert result3['min'] == 100.0
    assert result3['max'] == 200.0
    
    # Range with decimals
    result4 = handle_range("50.5-75.25")
    assert result4 is not None
    assert result4['min'] == 50.5
    assert result4['max'] == 75.25
    
    # Range with 'from...to'
    result5 = handle_range("from 10 to 20")
    assert result5 is not None
    assert result5['min'] == 10.0
    assert result5['max'] == 20.0
    
    # Range with 'between...and'
    result6 = handle_range("between 5 and 15")
    assert result6 is not None
    assert result6['min'] == 5.0
    assert result6['max'] == 15.0
    
    # No range found
    result7 = handle_range("single value 100")
    assert result7 is None
    
    result8 = handle_range("class A")
    assert result8 is None


def test_normalize_specification():
    """Test comprehensive specification normalization."""
    # Test case 1: '100.50 RUB'
    result1 = normalize_specification("100.50 RUB")
    assert result1['original'] == "100.50 RUB"
    assert result1['lowercase'] == "100.50 rub"
    assert result1['normalized'] == "100.50 rub"
    assert 'numeric_value' in result1
    assert result1['numeric_value']['value'] == 100.5
    assert result1['numeric_value']['unit'] == 'rub'
    assert 'range' not in result1
    
    # Test case 2: '80 g/m2'
    result2 = normalize_specification("80 g/m2")
    assert result2['original'] == "80 g/m2"
    assert result2['lowercase'] == "80 g/m2"
    assert result2['normalized'] == "80 g/m2"
    assert 'numeric_value' in result2
    assert result2['numeric_value']['value'] == 80.0
    assert result2['numeric_value']['unit'] == 'g/m2'
    assert 'range' not in result2
    
    # Test case 3: 'class A'
    result3 = normalize_specification("class A")
    assert result3['original'] == "class A"
    assert result3['lowercase'] == "class a"
    assert result3['normalized'] == "class a"
    assert 'numeric_value' not in result3
    assert 'range' not in result3
    
    # Test with range
    result4 = normalize_specification("10-20 кг")
    assert result4['original'] == "10-20 кг"
    assert result4['lowercase'] == "10-20 кг"
    assert result4['normalized'] == "10-20 kg"
    assert 'numeric_value' in result4
    assert result4['numeric_value']['value'] == 10.0  # First number in range
    assert result4['numeric_value']['unit'] == 'kg'
    assert 'range' in result4
    assert result4['range']['min'] == 10.0
    assert result4['range']['max'] == 20.0
    
    # Test complex case
    result5 = normalize_specification("Approx 500-750 мл воды")
    assert result5['original'] == "Approx 500-750 мл воды"
    assert result5['lowercase'] == "approx 500-750 мл воды"
    assert result5['normalized'] == "approx 500-750 ml воды"
    assert 'numeric_value' in result5
    assert result5['numeric_value']['value'] == 500.0
    assert result5['numeric_value']['unit'] == 'ml'  # Unit should be just 'ml', not 'ml воды'
    assert 'range' in result5
    assert result5['range']['min'] == 500.0
    assert result5['range']['max'] == 750.0


def test_integration():
    """Integration test with multiple functions."""
    text = "От 5 до 10 КГ муки"
    
    # Test individual functions
    lowercase = to_lowercase(text)
    assert lowercase == "от 5 до 10 кг муки"
    
    normalized = normalize_units(lowercase)
    assert normalized == "от 5 до 10 kg муки"
    
    numeric = extract_numeric_value(text)
    assert numeric is not None
    assert numeric['value'] == 5.0
    assert numeric['unit'] == 'kg'  # Unit should be just 'kg', not 'kg муки'
    
    range_val = handle_range(text)
    assert range_val is not None
    assert range_val['min'] == 5.0
    assert range_val['max'] == 10.0
    
    # Test comprehensive normalization
    full_result = normalize_specification(text)
    assert full_result['original'] == text
    assert full_result['lowercase'] == lowercase
    assert full_result['normalized'] == normalized
    assert 'numeric_value' in full_result
    assert 'range' in full_result


if __name__ == "__main__":
    pytest.main([__file__])