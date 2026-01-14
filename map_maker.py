"""
Map Maker Utility for Service Alpha
Handles data mapping and transformation between services
"""

def map_inventory_data(inventory_data):
    """
    Map inventory data from external service format to internal format
    Converts 'available_qty' field if present
    """
    mapped_data = {}
    
    # Map available_qty field if present
    if 'available_qty' in inventory_data:
        mapped_data['available_qty'] = inventory_data['available_qty']
    elif 'stock' in inventory_data:
        # Backward compatibility: convert 'stock' to 'available_qty'
        mapped_data['available_qty'] = inventory_data['stock']
    else:
        mapped_data['available_qty'] = 0
    
    # Copy other fields
    for key, value in inventory_data.items():
        if key not in ['stock', 'available_qty']:
            mapped_data[key] = value
    
    return mapped_data


def create_order_payload(item_id, available_qty):
    """
    Create order payload with available_qty information
    """
    return {
        'item_id': item_id,
        'available_qty': available_qty,
        'timestamp': '2024-01-01T00:00:00Z'  # Placeholder, should be actual timestamp
    }


def validate_available_qty(available_qty):
    """
    Validate that available_qty is a non-negative integer
    """
    if not isinstance(available_qty, (int, float)):
        return False
    if available_qty < 0:
        return False
    return True


if __name__ == '__main__':
    # Test the mapping functions
    test_data = {'available_qty': 10, 'item_name': 'Test Item'}
    mapped = map_inventory_data(test_data)
    print(f"Mapped data: {mapped}")
    
    # Test backward compatibility
    old_format_data = {'stock': 5, 'item_name': 'Old Item'}
    mapped_old = map_inventory_data(old_format_data)
    print(f"Mapped old format: {mapped_old}")