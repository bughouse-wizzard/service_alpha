"""
Normalization & Match Engine for comparing values.

Provides functions for normalizing strings (extracting numeric values and units)
and calculating match scores between target and actual values.
"""

import re
from typing import Optional, Tuple, Dict, Any
from rapidfuzz import fuzz


def normalize_value(value: str) -> Dict[str, Any]:
    """
    Normalize a string value by:
    1. Converting to lowercase
    2. Trimming whitespace
    3. Replacing ',' with '.'
    4. Extracting numeric value and unit using regex
    
    Args:
        value: Input string to normalize
        
    Returns:
        Dictionary with keys:
        - 'original': Original input string
        - 'normalized': Normalized string (lowercase, trimmed, commas replaced)
        - 'numeric_value': Extracted numeric value as float or None
        - 'unit': Extracted unit string or None
        - 'is_numeric': Boolean indicating if numeric value was found
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Step 1: Convert to lowercase and trim
    normalized = value.lower().strip()
    
    # Step 2: Replace commas with dots for decimal numbers
    normalized = normalized.replace(',', '.')
    
    # Step 3: Extract numeric value and unit using regex
    # Pattern matches: optional sign, digits, optional decimal, optional unit
    # Examples: "100 кг", "100.5 kg", "-50.25m", "75"
    numeric_pattern = r'^([+-]?\d*\.?\d+)\s*([a-zA-Zа-яА-ЯёЁ°%]*)$'
    match = re.match(numeric_pattern, normalized)
    
    result = {
        'original': value,
        'normalized': normalized,
        'numeric_value': None,
        'unit': None,
        'is_numeric': False
    }
    
    if match:
        numeric_str = match.group(1)
        unit = match.group(2).strip() if match.group(2) else None
        
        try:
            numeric_value = float(numeric_str)
            result['numeric_value'] = numeric_value
            result['unit'] = unit
            result['is_numeric'] = True
        except ValueError:
            # If conversion fails, treat as non-numeric
            pass
    
    return result


def calculate_match_score(
    target: str, 
    actual: str, 
    tolerance: float = 0.1,
    ai_qualitative_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Calculate match score between target and actual values.
    
    For numeric values: Check if within tolerance range (± tolerance * target_value)
    For text values: Use rapidfuzz.fuzz.token_sort_ratio for fuzzy matching
    
    Args:
        target: Target value to match against
        actual: Actual value to compare
        tolerance: Relative tolerance for numeric comparisons (default 0.1 = 10%)
        ai_qualitative_score: Optional AI assessment score (0-100) to combine with rule-based score
        
    Returns:
        Dictionary with match results including:
        - 'match_score': Final combined score (0-100)
        - 'rule_based_score': Score from rule-based matching (0-100)
        - 'ai_score': AI qualitative score if provided
        - 'is_match': Boolean indicating if values match (score >= 80)
        - 'match_type': Type of match ('exact', 'numeric', 'fuzzy', 'none')
        - 'details': Additional match details
    """
    # Normalize both values
    target_norm = normalize_value(target)
    actual_norm = normalize_value(actual)
    
    rule_based_score = 0
    match_type = 'none'
    details = {}
    
    # Case 1: Both are numeric values
    if target_norm['is_numeric'] and actual_norm['is_numeric']:
        target_val = target_norm['numeric_value']
        actual_val = actual_norm['numeric_value']
        
        # Check if units match (if both have units)
        unit_match = True
        if target_norm['unit'] and actual_norm['unit']:
            # Simple unit comparison - could be enhanced with unit conversion
            unit_match = target_norm['unit'] == actual_norm['unit']
            details['unit_match'] = unit_match
            details['target_unit'] = target_norm['unit']
            details['actual_unit'] = actual_norm['unit']
        
        # Calculate numeric match
        if target_val == 0:
            # Handle zero target value specially
            if actual_val == 0:
                numeric_score = 100
            else:
                numeric_score = 0
        else:
            relative_diff = abs(actual_val - target_val) / abs(target_val)
            if relative_diff <= tolerance:
                # Score decreases linearly from 100 to 80 as diff approaches tolerance
                numeric_score = 100 - (relative_diff / tolerance) * 20
                numeric_score = max(80, min(100, numeric_score))
            else:
                numeric_score = 0
        
        # Combine numeric score with unit match
        if unit_match:
            rule_based_score = numeric_score
            match_type = 'numeric' if numeric_score >= 80 else 'none'
        else:
            # Penalize for unit mismatch
            rule_based_score = numeric_score * 0.5
            match_type = 'none'
            
        details['relative_difference'] = relative_diff if target_val != 0 else 0
        details['tolerance'] = tolerance
        
    # Case 2: At least one is non-numeric - use text matching
    else:
        # Use token sort ratio for fuzzy string matching
        text_score = fuzz.token_sort_ratio(
            target_norm['normalized'], 
            actual_norm['normalized']
        )
        
        rule_based_score = text_score
        if text_score == 100:
            match_type = 'exact'
        elif text_score >= 80:
            match_type = 'fuzzy'
        else:
            match_type = 'none'
            
        details['text_similarity'] = text_score
    
    # Combine with AI qualitative assessment if provided
    final_score = rule_based_score
    if ai_qualitative_score is not None:
        # Simple weighted average: 70% rule-based, 30% AI assessment
        final_score = 0.7 * rule_based_score + 0.3 * ai_qualitative_score
        details['ai_qualitative_score'] = ai_qualitative_score
        details['weighting'] = '70% rule-based, 30% AI'
    
    # Determine if it's a match (threshold = 80)
    is_match = final_score >= 80
    
    return {
        'match_score': round(final_score, 2),
        'rule_based_score': round(rule_based_score, 2),
        'ai_score': ai_qualitative_score,
        'is_match': is_match,
        'match_type': match_type,
        'details': details,
        'target_normalized': target_norm,
        'actual_normalized': actual_norm
    }