from flask import Flask, jsonify
import map_maker

app = Flask(__name__)

# Sample inventory data - in a real app, this would be from a database
INVENTORY_DATA = {
    "item_001": {"available_qty": 15},
    "item_002": {"available_qty": 0},
    "item_003": {"available_qty": 42},
    "item_004": {"stock": 25},  # Legacy field name for backward compatibility
    "item_005": {"available_qty": "30"},  # String value that should be converted
    "item_006": {"available_qty": 12.7},  # Float value that should be converted
}

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    """
    Get inventory information for an item.
    
    Args:
        item_id: The item identifier
    
    Returns:
        JSON response with item_id and available_qty
    """
    # Get inventory data for the item
    item_data = INVENTORY_DATA.get(item_id, {})
    
    # Always include item_id in response
    response_data = {"item_id": item_id}
    
    # Add available_qty or stock field from inventory data
    if 'available_qty' in item_data:
        response_data['available_qty'] = item_data['available_qty']
    elif 'stock' in item_data:
        # For backward compatibility, include both field names
        response_data['stock'] = item_data['stock']
        response_data['available_qty'] = item_data['stock']
    
    # Use map_maker to validate and process the response
    definitions = map_maker.get_definitions(response_data)
    
    # Check if there are any validation or conversion errors
    available_qty_info = definitions["fields"].get("available_qty", {})
    
    # Add metadata about the processing if there were issues
    if 'validation_error' in available_qty_info:
        response_data['validation_warning'] = available_qty_info['validation_error']
    if 'conversion_error' in available_qty_info:
        response_data['conversion_warning'] = available_qty_info['conversion_error']
    
    # Ensure available_qty is properly formatted (integer)
    if 'available_qty' in response_data:
        try:
            # Convert to integer if possible
            response_data['available_qty'] = int(float(response_data['available_qty']))
        except (ValueError, TypeError):
            # If conversion fails, keep original value but add warning
            if 'conversion_warning' not in response_data:
                response_data['conversion_warning'] = f"Could not convert available_qty to integer: {response_data['available_qty']}"
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5002)
