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
        definitions["fields"]["available_qty"]["current_value"] = data_source['available_qty']
    elif 'stock' in data_source:
        # Backward compatibility: map 'stock' field to 'available_qty'
        definitions["fields"]["available_qty"]["current_value"] = data_source['stock']
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


if __name__ == "__main__":
    # Test the function with new field name
    print("Test 1: New field name 'available_qty'")
    test_data = {"item_id": "TEST123", "available_qty": 15}
    definitions = get_definitions(test_data)

    print("Field Definitions:")
    for field, info in definitions["fields"].items():
        print(f"  {field}: {info.get('description', 'No description')}")

    # Test backward compatibility with old 'stock' field name
    print("\nTest 2: Backward compatibility with 'stock' field")
    test_data_legacy = {"item_id": "TEST456", "stock": 25}
    definitions_legacy = get_definitions(test_data_legacy)

    print("Field Definitions (with legacy 'stock' field):")
    for field, info in definitions_legacy["fields"].items():
        desc = info.get('description', 'No description')
        if field == 'available_qty' and 'legacy_field' in info:
            desc += f" (mapped from legacy field: {info['legacy_field']})"
        print(f"  {field}: {desc}")