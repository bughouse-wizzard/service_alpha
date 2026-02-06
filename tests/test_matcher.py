"""
Unit tests for the matcher.py module.
"""

import pytest
from app.services.matcher import normalize_value, calculate_match_score


class TestNormalizeValue:
    """Test cases for normalize_value function."""
    
    def test_normalize_lowercase_and_trim(self):
        """Test that values are converted to lowercase and trimmed."""
        result = normalize_value("  HELLO WORLD  ")
        assert result['normalized'] == "hello world"
        assert result['original'] == "  HELLO WORLD  "
    
    def test_replace_commas_with_dots(self):
        """Test that commas are replaced with dots for decimal numbers."""
        result = normalize_value("100,5 кг")
        assert result['normalized'] == "100.5 кг"
    
    def test_extract_numeric_value_with_unit(self):
        """Test extraction of numeric value and unit."""
        result = normalize_value("100 кг")
        assert result['numeric_value'] == 100.0
        assert result['unit'] == 'кг'
        assert result['is_numeric'] is True
    
    def test_extract_numeric_value_with_decimal(self):
        """Test extraction of decimal numeric value."""
        result = normalize_value("100.50 kilogram")
        assert result['numeric_value'] == 100.5
        assert result['unit'] == 'kilogram'
        assert result['is_numeric'] is True
    
    def test_extract_numeric_value_with_negative(self):
        """Test extraction of negative numeric value."""
        result = normalize_value("-50.25m")
        assert result['numeric_value'] == -50.25
        assert result['unit'] == 'm'
        assert result['is_numeric'] is True
    
    def test_extract_numeric_value_no_unit(self):
        """Test extraction of numeric value without unit."""
        result = normalize_value("75")
        assert result['numeric_value'] == 75.0
        assert result['unit'] is None
        assert result['is_numeric'] is True
    
    def test_non_numeric_value(self):
        """Test non-numeric value."""
        result = normalize_value("Sony")
        assert result['numeric_value'] is None
        assert result['unit'] is None
        assert result['is_numeric'] is False
        assert result['normalized'] == "sony"
    
    def test_mixed_case_unit(self):
        """Test value with mixed case unit."""
        result = normalize_value("100 KG")
        assert result['numeric_value'] == 100.0
        assert result['unit'] == 'kg'
        assert result['is_numeric'] is True


class TestCalculateMatchScore:
    """Test cases for calculate_match_score function."""
    
    def test_numeric_exact_match_with_same_units(self):
        """Test exact numeric match with same units."""
        result = calculate_match_score("100 кг", "100 кг")
        assert result['is_match'] is True
        assert result['match_score'] == 100
        assert result['match_type'] == 'numeric'
        assert result['rule_based_score'] == 100
    
    def test_numeric_exact_match_different_format(self):
        """Test exact numeric match with different formatting."""
        result = calculate_match_score("100 кг", "100.00 kilogram")
        # This should match because 100 == 100.00, but units are different
        # Units don't match ('кг' vs 'kilogram'), so score should be reduced
        assert result['is_match'] is False  # Unit mismatch reduces score below 80
        assert result['match_type'] == 'none'
        assert 'unit_match' in result['details']
        assert result['details']['unit_match'] is False
    
    def test_numeric_within_tolerance(self):
        """Test numeric values within tolerance range."""
        result = calculate_match_score("100 кг", "95 кг", tolerance=0.1)
        # 95 is within 10% of 100 (90-110), so should match
        assert result['is_match'] is True
        assert result['match_type'] == 'numeric'
        assert 80 <= result['match_score'] <= 100
    
    def test_numeric_outside_tolerance(self):
        """Test numeric values outside tolerance range."""
        result = calculate_match_score("100 кг", "50 кг", tolerance=0.1)
        # 50 is outside 10% of 100, so should not match
        assert result['is_match'] is False
        assert result['match_type'] == 'none'
        assert result['match_score'] < 80
    
    def test_text_exact_match(self):
        """Test exact text match."""
        result = calculate_match_score("Sony", "Sony")
        assert result['is_match'] is True
        assert result['match_score'] == 100
        assert result['match_type'] == 'exact'
    
    def test_text_fuzzy_match(self):
        """Test fuzzy text match."""
        result = calculate_match_score("apple", "appel")
        # "appel" is similar to "apple" - should be a fuzzy match
        assert result['is_match'] is True  # Should be above 80 threshold
        assert result['match_type'] == 'fuzzy'
        assert result['match_score'] >= 80
    
    def test_text_no_match(self):
        """Test text with no match."""
        result = calculate_match_score("Sony", "Microsoft")
        # Very different strings - should not match
        assert result['is_match'] is False
        assert result['match_type'] == 'none'
        assert result['match_score'] < 80
    
    def test_combination_with_ai_score(self):
        """Test combination of rule-based score with AI qualitative assessment."""
        # Test case where rule-based score is 70 and AI score is 90
        result = calculate_match_score("test", "tst", ai_qualitative_score=90)
        
        # Rule-based score for "test" vs "tst" should be fuzzy but below 80
        # With AI score of 90, combined score should be higher
        assert 'ai_qualitative_score' in result['details']
        assert result['details']['ai_qualitative_score'] == 90
        assert 'weighting' in result['details']
        
        # Calculate expected combined score: 0.7 * rule_based + 0.3 * 90
        rule_based = result['rule_based_score']
        expected = 0.7 * rule_based + 0.3 * 90
        assert abs(result['match_score'] - expected) < 0.1
    
    def test_zero_target_value(self):
        """Test matching with zero target value."""
        result = calculate_match_score("0 кг", "0 кг")
        assert result['is_match'] is True
        assert result['match_score'] == 100
        assert result['match_type'] == 'numeric'
    
    def test_zero_target_nonzero_actual(self):
        """Test matching zero target with non-zero actual."""
        result = calculate_match_score("0 кг", "10 кг")
        assert result['is_match'] is False
        assert result['match_score'] == 0
    
    def test_special_characters_and_spaces(self):
        """Test values with special characters and extra spaces."""
        result = normalize_value("  100,5  kg  ")
        assert result['normalized'] == "100.5  kg"
        assert result['numeric_value'] == 100.5
        assert result['unit'] == 'kg'
    
    def test_match_score_structure(self):
        """Test that match score result has expected structure."""
        result = calculate_match_score("100 кг", "100 кг")
        
        expected_keys = {
            'match_score', 'rule_based_score', 'ai_score', 'is_match',
            'match_type', 'details', 'target_normalized', 'actual_normalized'
        }
        
        assert set(result.keys()) == expected_keys
        assert isinstance(result['details'], dict)
        assert isinstance(result['target_normalized'], dict)
        assert isinstance(result['actual_normalized'], dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])