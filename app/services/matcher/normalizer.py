"""
String normalization utilities for specification matching.
"""

import re
from typing import Dict, Optional, Tuple, Union


def to_lowercase(text: str) -> str:
    """
    Convert string to lowercase.
    
    Args:
        text: Input string
        
    Returns:
        Lowercase string
    """
    return text.lower()


def normalize_units(text: str) -> str:
    """
    Normalize units in a string.
    
    Converts various unit representations to standard forms:
    - 'кг', 'килограмм', 'kilogram' -> 'kg'
    - 'г', 'грамм', 'gram' -> 'g'
    - 'л', 'литр', 'liter' -> 'l'
    - 'мл', 'миллилитр', 'milliliter' -> 'ml'
    - 'м', 'метр', 'meter' -> 'm'
    - 'см', 'сантиметр', 'centimeter' -> 'cm'
    - 'мм', 'миллиметр', 'millimeter' -> 'mm'
    - 'руб', 'рубль', 'ruble' -> 'rub'
    - 'usd', 'доллар', 'dollar' -> 'usd'
    - 'eur', 'евро', 'euro' -> 'eur'
    
    Args:
        text: Input string
        
    Returns:
        String with normalized units
    """
    # Dictionary of unit mappings - order matters for compound units
    # Process compound units first, then simple units
    unit_mappings = [
        # Compound units (need to be processed first)
        (r'\bкв\.?м\b|\bквадратный метр\b', 'm2'),
        (r'\bкв\.?см\b|\bквадратный сантиметр\b', 'cm2'),
        (r'\bм2\b|\bм²\b', 'm2'),
        (r'\bсм2\b|\bсм²\b', 'cm2'),
        
        # Weight units
        (r'\bкг\b|\bкилограмм\b|\bkilogram\b', 'kg'),
        (r'\bг\b|\bграмм\b|\bgram\b', 'g'),
        (r'\bт\b|\bтонн\b|\bton\b', 't'),
        
        # Volume units
        (r'\bл\b|\bлитр\b|\bliter\b', 'l'),
        (r'\bмл\b|\bмиллилитр\b|\bmilliliter\b', 'ml'),
        
        # Length units
        (r'\bм\b|\bметр\b|\bmeter\b', 'm'),
        (r'\bсм\b|\bсантиметр\b|\bcentimeter\b', 'cm'),
        (r'\bмм\b|\bмиллиметр\b|\bmillimeter\b', 'mm'),
        
        # Currency units
        (r'\bруб\b|\bрубль\b|\bruble\b', 'rub'),
        (r'\bр\b|\bрублей\b', 'rub'),
        (r'\busd\b|\bдоллар\b|\bdollar\b', 'usd'),
        (r'\$', 'usd'),
        (r'\beur\b|\bевро\b|\beuro\b', 'eur'),
        (r'€', 'eur'),
        
        # Other common units
        (r'\bшт\b|\bштук\b|\bpiece\b', 'pcs'),
        (r'\bуп\b|\bупаковк\b|\bpack\b', 'pack'),
        (r'\bпач\b|\bпачка\b', 'pack'),
    ]
    
    # Additional patterns without word boundaries for units attached to numbers
    attached_unit_mappings = [
        (r'(?<=\d)л\b', 'l'),  # "5л" -> "5l"
        (r'(?<=\d)мл\b', 'ml'),  # "250мл" -> "250ml"
        (r'(?<=\d)кг\b', 'kg'),  # "10кг" -> "10kg"
        (r'(?<=\d)г\b', 'g'),  # "500г" -> "500g"
        (r'(?<=\d)м\b', 'm'),  # "5м" -> "5m"
        (r'(?<=\d)см\b', 'cm'),  # "30см" -> "30cm"
        (r'(?<=\d)мм\b', 'mm'),  # "100мм" -> "100mm"
        (r'(?<=\d)руб\b', 'rub'),  # "100руб" -> "100rub"
    ]
    
    normalized_text = text.lower()
    
    # First apply regular unit mappings
    for pattern, replacement in unit_mappings:
        normalized_text = re.sub(pattern, replacement, normalized_text, flags=re.IGNORECASE)
    
    # Then apply attached unit mappings (units directly after numbers)
    for pattern, replacement in attached_unit_mappings:
        normalized_text = re.sub(pattern, replacement, normalized_text, flags=re.IGNORECASE)
    
    return normalized_text


def extract_numeric_value(text: str) -> Optional[Dict[str, Union[float, str]]]:
    """
    Extract numeric value and unit from a string.
    
    Examples:
        'approx 500 ml' -> {'value': 500.0, 'unit': 'ml'}
        '100.50 RUB' -> {'value': 100.5, 'unit': 'rub'}
        '80 g/m2' -> {'value': 80.0, 'unit': 'g/m2'}
        
    Args:
        text: Input string
        
    Returns:
        Dictionary with 'value' (float) and 'unit' (str) keys,
        or None if no numeric value found
    """
    # First normalize the text
    normalized_text = normalize_units(to_lowercase(text))
    
    # Pattern to match numbers (including decimals and negative numbers)
    # This pattern captures: optional sign, digits with optional decimal point
    number_pattern = r'[-+]?\d*\.?\d+'
    
    # Find all numbers in the text
    numbers = re.findall(number_pattern, normalized_text)
    
    if not numbers:
        return None
    
    # Take the first number found
    try:
        value = float(numbers[0])
    except ValueError:
        return None
    
    # Find the position of the first number
    match = re.search(number_pattern, normalized_text)
    if not match:
        return None
    
    # Extract unit - look for common unit patterns near the number
    # First, get a window of text around the number (up to 30 chars after)
    start_pos = match.start()
    end_pos = match.end()
    
    # Look ahead for unit patterns in a larger window
    lookahead_window = normalized_text[end_pos:end_pos + 50]
    
    # Common unit patterns - more flexible matching
    unit_patterns = [
        # Temperature units (with optional degree symbol)
        r'°[cf]',  # °c or °f
        r'°',  # Just degree symbol
        
        # Percentage
        r'%',
        
        # Standard units (1-5 letters, optional digits, optional slash)
        # Match even if there's some text before the unit
        r'([a-zA-Z]{1,5}\d*[/\\]?[a-zA-Z]{0,5}\d*\b)',  # kg, g/m2, m2, etc.
        r'([a-zA-Z]{1,5}\b)',  # Simple units like kg, g, m, etc.
    ]
    
    unit = ''
    for pattern in unit_patterns:
        unit_match = re.search(pattern, lookahead_window)
        if unit_match:
            # Extract the unit from the match
            if unit_match.groups():
                unit = unit_match.group(1).strip()
            else:
                unit = unit_match.group(0).strip()
            break
    
    # If still no unit found, try a different approach:
    # Look for common unit abbreviations in the entire text
    if not unit:
        common_units = ['kg', 'g', 'l', 'ml', 'm', 'cm', 'mm', 'rub', 'usd', 'eur', 'm2', 'cm2']
        for common_unit in common_units:
            if common_unit in normalized_text:
                # Check if this unit is reasonably close to our number
                unit_pos = normalized_text.find(common_unit)
                if abs(unit_pos - end_pos) < 20:  # Within 20 characters
                    unit = common_unit
                    break
    
    # Clean up the unit
    unit = unit.strip(' .,;:!?-')
    
    return {
        'value': value,
        'unit': unit if unit else ''
    }


def handle_range(text: str) -> Optional[Dict[str, float]]:
    """
    Handle ranges in strings.
    
    Examples:
        '10-20' -> {'min': 10.0, 'max': 20.0}
        '5 to 15' -> {'min': 5.0, 'max': 15.0}
        '100-150.5' -> {'min': 100.0, 'max': 150.5}
        
    Args:
        text: Input string
        
    Returns:
        Dictionary with 'min' and 'max' keys,
        or None if no range found
    """
    # Normalize the text first
    normalized_text = to_lowercase(text)
    
    # Patterns for ranges
    range_patterns = [
        # Pattern for "X-Y" or "X - Y"
        r'(\d*\.?\d+)\s*[-–—]\s*(\d*\.?\d+)',
        # Pattern for "X to Y" (English)
        r'(\d*\.?\d+)\s+to\s+(\d*\.?\d+)',
        # Pattern for "X до Y" (Russian)
        r'(\d*\.?\d+)\s+до\s+(\d*\.?\d+)',
        # Pattern for "X...Y" or "X..Y"
        r'(\d*\.?\d+)\s*\.{2,3}\s*(\d*\.?\d+)',
        # Pattern for "from X to Y"
        r'from\s+(\d*\.?\d+)\s+to\s+(\d*\.?\d+)',
        # Pattern for "between X and Y"
        r'between\s+(\d*\.?\d+)\s+and\s+(\d*\.?\d+)',
        # Pattern for "от X до Y" (Russian "from X to Y")
        r'от\s+(\d*\.?\d+)\s+до\s+(\d*\.?\d+)',
    ]
    
    for pattern in range_patterns:
        match = re.search(pattern, normalized_text)
        if match:
            try:
                min_val = float(match.group(1))
                max_val = float(match.group(2))
                return {'min': min_val, 'max': max_val}
            except ValueError:
                continue
    
    return None


def normalize_specification(text: str) -> Dict:
    """
    Comprehensive normalization of a specification string.
    
    Applies all normalization functions and returns a structured result.
    
    Args:
        text: Input specification string
        
    Returns:
        Dictionary with normalized information including:
        - original: original text
        - lowercase: lowercase version
        - normalized: fully normalized text
        - numeric_value: extracted numeric value and unit (if any)
        - range: extracted range (if any)
    """
    result = {
        'original': text,
        'lowercase': to_lowercase(text),
        'normalized': normalize_units(to_lowercase(text)),
    }
    
    # Extract numeric value
    numeric_value = extract_numeric_value(text)
    if numeric_value:
        result['numeric_value'] = numeric_value
    
    # Extract range
    range_value = handle_range(text)
    if range_value:
        result['range'] = range_value
    
    return result