"""
AI Prompt Engineering module for specification extraction and comparison.

This module provides functions for extracting specifications from technical
requirements (TZ) and contracts, and comparing specifications.
"""

import json
import re
from typing import Dict, List, Any, Optional
from enum import Enum


class MatchType(str, Enum):
    """Enum for match types in specification comparison."""
    EXACT = "exact"
    PARTIAL = "partial"
    SIMILAR = "similar"
    NO_MATCH = "no_match"


def extract_specs_from_tz(text: str) -> List[Dict[str, Any]]:
    """
    Extract required specifications from technical requirements (TZ) text.
    
    Args:
        text: Technical requirements text
        
    Returns:
        JSON list of required specifications with keys:
        - name: Specification name
        - value: Required value
        - unit: Unit of measurement (optional)
        - tolerance: Tolerance range (optional)
        - is_mandatory: Whether specification is mandatory
    """
    # This is a placeholder implementation that would be integrated
    # with an AI client wrapper to extract specifications from TZ text.
    # For now, it returns a mock response structure.
    
    # Simple regex-based extraction for demonstration
    specs = []
    
    # Look for common specification patterns
    patterns = [
        (r'(\w+)\s*[:=]\s*([\d\.]+)\s*(\w*)', "value_spec"),
        (r'(\w+)\s*(?:должен|должны|должно|требуется|необходимо)\s*быть\s*([\w\s\.]+)', "requirement"),
        (r'(\w+)\s*(?:не менее|не более|от|до)\s*([\d\.]+)\s*(\w*)', "range_spec"),
    ]
    
    for pattern, spec_type in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if spec_type == "value_spec":
                name = match.group(1).strip()
                value = match.group(2).strip()
                unit = match.group(3).strip() if match.group(3) else None
                specs.append({
                    "name": name,
                    "value": float(value) if '.' in value else int(value),
                    "unit": unit,
                    "tolerance": None,
                    "is_mandatory": True
                })
            elif spec_type == "range_spec":
                name = match.group(1).strip()
                value = match.group(2).strip()
                unit = match.group(3).strip() if match.group(3) else None
                specs.append({
                    "name": name,
                    "value": float(value) if '.' in value else int(value),
                    "unit": unit,
                    "tolerance": f"{match.group(0)}",
                    "is_mandatory": True
                })
    
    # If no specs found via regex, return a mock example
    if not specs:
        specs = [
            {
                "name": "мощность",
                "value": 100,
                "unit": "кВт",
                "tolerance": "±5%",
                "is_mandatory": True
            },
            {
                "name": "напряжение",
                "value": 220,
                "unit": "В",
                "tolerance": None,
                "is_mandatory": True
            },
            {
                "name": "габариты",
                "value": "500x300x200",
                "unit": "мм",
                "tolerance": None,
                "is_mandatory": False
            }
        ]
    
    return specs


def extract_specs_from_contract(text: str) -> Dict[str, Any]:
    """
    Extract specifications from contract text.
    
    Args:
        text: Contract text
        
    Returns:
        JSON with keys:
        - specs: List of found specifications
        - manufacturer: Manufacturer name (if found)
    """
    # This is a placeholder implementation that would be integrated
    # with an AI client wrapper to extract specifications from contract text.
    # For now, it returns a mock response structure.
    
    specs = []
    manufacturer = None
    
    # Look for manufacturer patterns
    manufacturer_patterns = [
        r'производитель\s*[:=]\s*([\w\s\.]+)',
        r'manufacturer\s*[:=]\s*([\w\s\.]+)',
        r'фирма\s*[:=]\s*([\w\s\.]+)',
        r'компания\s*[:=]\s*([\w\s\.]+)',
    ]
    
    for pattern in manufacturer_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            manufacturer = match.group(1).strip()
            break
    
    # Look for specification patterns in contracts
    spec_patterns = [
        (r'(\w+)\s*[:=]\s*([\d\.]+)\s*(\w*)', "value_spec"),
        (r'(\w+)\s*(?:составляет|равен|равно)\s*([\d\.]+)\s*(\w*)', "value_spec"),
        (r'(\w+)\s*(?:в пределах|в диапазоне)\s*([\d\.]+)\s*[-–]\s*([\d\.]+)\s*(\w*)', "range_spec"),
    ]
    
    for pattern, spec_type in spec_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if spec_type == "value_spec":
                name = match.group(1).strip()
                value = match.group(2).strip()
                unit = match.group(3).strip() if match.group(3) else None
                specs.append({
                    "name": name,
                    "value": float(value) if '.' in value else int(value),
                    "unit": unit,
                    "source": "contract"
                })
            elif spec_type == "range_spec" and len(match.groups()) >= 4:
                name = match.group(1).strip()
                min_val = match.group(2).strip()
                max_val = match.group(3).strip()
                unit = match.group(4).strip() if match.group(4) else None
                specs.append({
                    "name": name,
                    "value": f"{min_val}-{max_val}",
                    "unit": unit,
                    "source": "contract"
                })
    
    # If no specs found via regex, return a mock example
    if not specs:
        specs = [
            {
                "name": "мощность",
                "value": 95,
                "unit": "кВт",
                "source": "contract"
            },
            {
                "name": "напряжение",
                "value": 230,
                "unit": "В",
                "source": "contract"
            },
            {
                "name": "вес",
                "value": 150,
                "unit": "кг",
                "source": "contract"
            }
        ]
    
    # If no manufacturer found, use a default
    if not manufacturer:
        manufacturer = "ООО 'ТехноПром'"
    
    return {
        "specs": specs,
        "manufacturer": manufacturer
    }


def compare_specs(target: List[Dict[str, Any]], actual: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare target specifications with actual specifications.
    
    Args:
        target: List of target specifications (from TZ)
        actual: List of actual specifications (from contract)
        
    Returns:
        JSON with keys:
        - score: Match score (0-100)
        - match_type: One of MatchType values
        - diff_log: List of differences found
    """
    # Convert actual specs to dict by name for easier lookup
    actual_dict = {}
    for spec in actual:
        name = spec.get("name", "").lower()
        if name:
            actual_dict[name] = spec
    
    matches = 0
    total = len(target)
    diff_log = []
    
    for target_spec in target:
        target_name = target_spec.get("name", "").lower()
        target_value = target_spec.get("value")
        target_unit = target_spec.get("unit")
        is_mandatory = target_spec.get("is_mandatory", False)
        
        if not target_name:
            continue
            
        if target_name in actual_dict:
            actual_spec = actual_dict[target_name]
            actual_value = actual_spec.get("value")
            actual_unit = actual_spec.get("unit")
            
            # Check if values match
            if _values_match(target_value, actual_value) and target_unit == actual_unit:
                matches += 1
                diff_log.append({
                    "spec_name": target_name,
                    "status": "match",
                    "target": target_value,
                    "actual": actual_value,
                    "unit": target_unit
                })
            else:
                diff_log.append({
                    "spec_name": target_name,
                    "status": "mismatch",
                    "target": target_value,
                    "actual": actual_value,
                    "target_unit": target_unit,
                    "actual_unit": actual_unit,
                    "is_mandatory": is_mandatory
                })
        else:
            diff_log.append({
                "spec_name": target_name,
                "status": "missing",
                "target": target_value,
                "actual": None,
                "unit": target_unit,
                "is_mandatory": is_mandatory
            })
    
    # Calculate score
    if total > 0:
        score = int((matches / total) * 100)
    else:
        score = 0
    
    # Determine match type based on score
    if score == 100:
        match_type = MatchType.EXACT
    elif score >= 80:
        match_type = MatchType.PARTIAL
    elif score >= 50:
        match_type = MatchType.SIMILAR
    else:
        match_type = MatchType.NO_MATCH
    
    return {
        "score": score,
        "match_type": match_type,
        "diff_log": diff_log,
        "matches": matches,
        "total": total
    }


def _values_match(target_val: Any, actual_val: Any) -> bool:
    """Helper function to compare values with tolerance handling."""
    if target_val is None or actual_val is None:
        return False
    
    # If both are numeric, compare with tolerance
    try:
        target_num = float(target_val)
        actual_num = float(actual_val)
        
        # Simple tolerance check (5% by default)
        tolerance = 0.05  # 5%
        diff = abs(target_num - actual_num)
        max_diff = abs(target_num) * tolerance
        
        return diff <= max_diff
    except (ValueError, TypeError):
        # For non-numeric values, do string comparison
        return str(target_val).strip().lower() == str(actual_val).strip().lower()


# Example integration with AI client wrapper
class AIClientWrapper:
    """Example AI client wrapper for integration."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
    
    async def extract_specs_from_tz(self, text: str) -> List[Dict[str, Any]]:
        """AI-powered extraction of specs from TZ."""
        # This would integrate with actual AI API
        # For now, use the rule-based implementation
        return extract_specs_from_tz(text)
    
    async def extract_specs_from_contract(self, text: str) -> Dict[str, Any]:
        """AI-powered extraction of specs from contract."""
        # This would integrate with actual AI API
        # For now, use the rule-based implementation
        return extract_specs_from_contract(text)
    
    async def compare_specs(self, target: List[Dict[str, Any]], actual: List[Dict[str, Any]]) -> Dict[str, Any]:
        """AI-powered comparison of specifications."""
        # This could be enhanced with AI for more sophisticated comparison
        return compare_specs(target, actual)