"""
Map Maker Module
Handles data mapping and definitions for the service_beta application.
"""

def get_definitions(data_source=None):
    """
    Get field definitions for the application.
    
    Args:
        data_source (dict, optional): Source data to analyze for field definitions.
    
    Returns:
        dict: Field definitions with mappings and metadata.
    """
    # Base definitions
    definitions = {
        "fields": {
            "item_id": {
                "type": "string",
                "required": True,
                "description": "Unique identifier for the item"
            },
            "available_qty": {
                "type": "integer",
                "required": True,
                "description": "Available quantity for ordering",
                "min_value": 0
            }
        },
        "endpoints": {
            "inventory": {
                "method": "GET",
                "path": "/inventory/{item_id}",
                "returns": ["item_id", "available_qty"]
            }
        }
    }
    
    # If data_source is provided, analyze it for additional field information
    if data_source:
        definitions = _analyze_data_source(data_source, definitions)
    
    return definitions


def _analyze_data_source(data_source, definitions):
    """
    Analyze data source to extract field information.
    
    Args:
        data_source (dict): Source data to analyze
        definitions (dict): Current definitions to update
    
    Returns:
        dict: Updated definitions
    """
    if not isinstance(data_source, dict):
        return definitions
    
    # Check for available_qty field (new standard)
    # Also handle backward compatibility with 'stock' field name
    if 'available_qty' in data_source:
        definitions = _process_available_qty(data_source['available_qty'], definitions, is_legacy=False)
    elif 'stock' in data_source:
        # Backward compatibility: map 'stock' field to 'available_qty'
        definitions = _process_available_qty(data_source['stock'], definitions, is_legacy=True)
        definitions["fields"]["available_qty"]["legacy_field"] = "stock"
    
    # Add any additional fields from data_source
    # Skip 'stock' field if it was already mapped to 'available_qty'
    for field, value in data_source.items():
        if field == 'stock' and 'legacy_field' in definitions["fields"]["available_qty"]:
            # Skip adding 'stock' as separate field since it was mapped to available_qty
            continue
        if field not in definitions["fields"]:
            definitions["fields"][field] = {
                "type": type(value).__name__,
                "value": value,
                "description": f"Additional field from data source"
            }
    
    return definitions


def _process_available_qty(value, definitions, is_legacy=False):
    """
    Process available_qty value with proper type conversion and validation.
    
    Args:
        value: The available_qty value to process
        definitions (dict): Current definitions to update
        is_legacy (bool): Whether this is from a legacy 'stock' field
    
    Returns:
        dict: Updated definitions
    """
    try:
        # Convert to integer if possible
        if isinstance(value, (int, float, str)):
            int_value = int(float(value))  # Handle strings and floats
        else:
            int_value = value
        
        # Validate min_value constraint
        min_val = definitions["fields"]["available_qty"].get("min_value", 0)
        if isinstance(int_value, (int, float)) and int_value < min_val:
            definitions["fields"]["available_qty"]["validation_error"] = f"Value {int_value} is below minimum {min_val}"
            definitions["fields"]["available_qty"]["current_value"] = int_value
        else:
            definitions["fields"]["available_qty"]["current_value"] = int_value
            
        # Add type information
        definitions["fields"]["available_qty"]["original_type"] = type(value).__name__
        definitions["fields"]["available_qty"]["processed_type"] = type(int_value).__name__
        
    except (ValueError, TypeError) as e:
        # Handle conversion errors
        definitions["fields"]["available_qty"]["conversion_error"] = str(e)
        definitions["fields"]["available_qty"]["current_value"] = value
        definitions["fields"]["available_qty"]["original_type"] = type(value).__name__
    
    return definitions


if __name__ == "__main__":
    # Test the function with new field name
    print("Test 1: New field name 'available_qty' as integer")
    test_data = {"item_id": "TEST123", "available_qty": 15}
    definitions = get_definitions(test_data)
    
    print("Field Definitions:")
    for field, info in definitions["fields"].items():
        desc = info.get('description', 'No description')
        if field == 'available_qty':
            current_val = info.get('current_value', 'N/A')
            orig_type = info.get('original_type', 'N/A')
            proc_type = info.get('processed_type', 'N/A')
            desc += f" | Value: {current_val} (original: {orig_type}, processed: {proc_type})"
        print(f"  {field}: {desc}")
    
    # Test backward compatibility with old 'stock' field name
    print("\nTest 2: Backward compatibility with 'stock' field")
    test_data_legacy = {"item_id": "TEST456", "stock": 25}
    definitions_legacy = get_definitions(test_data_legacy)
    
    print("Field Definitions (with legacy 'stock' field):")
    for field, info in definitions_legacy["fields"].items():
        desc = info.get('description', 'No description')
        if field == 'available_qty':
            if 'legacy_field' in info:
                desc += f" (mapped from legacy field: {info['legacy_field']})"
            current_val = info.get('current_value', 'N/A')
            orig_type = info.get('original_type', 'N/A')
            proc_type = info.get('processed_type', 'N/A')
            desc += f" | Value: {current_val} (original: {orig_type}, processed: {proc_type})"
        print(f"  {field}: {desc}")
    
    # Additional tests for type conversion and validation
    print("\nTest 3: available_qty as string '30'")
    test_data_str = {"item_id": "TEST789", "available_qty": "30"}
    definitions_str = get_definitions(test_data_str)
    available_qty_info = definitions_str["fields"]["available_qty"]
    print(f"  Original value: '30' (type: {available_qty_info.get('original_type')})")
    print(f"  Processed value: {available_qty_info.get('current_value')} (type: {available_qty_info.get('processed_type')})")
    
    print("\nTest 4: available_qty as float 12.7")
    test_data_float = {"item_id": "TEST999", "available_qty": 12.7}
    definitions_float = get_definitions(test_data_float)
    available_qty_info = definitions_float["fields"]["available_qty"]
    print(f"  Original value: 12.7 (type: {available_qty_info.get('original_type')})")
    print(f"  Processed value: {available_qty_info.get('current_value')} (type: {available_qty_info.get('processed_type')})")
    
    print("\nTest 5: available_qty as negative number -5")
    test_data_neg = {"item_id": "TEST000", "available_qty": -5}
    definitions_neg = get_definitions(test_data_neg)
    available_qty_info = definitions_neg["fields"]["available_qty"]
    print(f"  Value: {available_qty_info.get('current_value')}")
    print(f"  Validation error: {available_qty_info.get('validation_error', 'No error')}")
    
    print("\nTest 6: stock as string '42' (legacy)")
    test_data_stock_str = {"item_id": "TEST111", "stock": "42"}
    definitions_stock_str = get_definitions(test_data_stock_str)
    available_qty_info = definitions_stock_str["fields"]["available_qty"]
    print(f"  Original value: '42' (type: {available_qty_info.get('original_type')})")
    print(f"  Processed value: {available_qty_info.get('current_value')} (type: {available_qty_info.get('processed_type')})")
    print(f"  Legacy field: {available_qty_info.get('legacy_field', 'N/A')}")