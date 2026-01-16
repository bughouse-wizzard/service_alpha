"""
Service Beta (Inventory Service)
This service runs on port 5002 and provides inventory data.
Returns 'available_qty' field instead of 'stock' to align with new enterprise standards.
"""
from flask import Flask, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock inventory database
INVENTORY_DB = {
    "item_001": {"name": "Laptop", "available_qty": 5, "price": 999.99},
    "item_002": {"name": "Mouse", "available_qty": 50, "price": 29.99},
    "item_003": {"name": "Keyboard", "available_qty": 25, "price": 79.99},
    "item_004": {"name": "Monitor", "available_qty": 0, "price": 299.99},  # Out of stock
    "item_005": {"name": "Headphones", "available_qty": 15, "price": 149.99},
}

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    """Get inventory for a specific item"""
    logger.info(f"Received inventory request for item_id: {item_id}")
    
    if item_id in INVENTORY_DB:
        item_data = INVENTORY_DB[item_id]
        logger.info(f"Returning inventory for {item_id}: {item_data}")
        return jsonify({
            "item_id": item_id,
            "name": item_data["name"],
            "available_qty": item_data["available_qty"],
            "price": item_data["price"],
            "in_stock": item_data["available_qty"] > 0
        })
    else:
        logger.warning(f"Item not found: {item_id}")
        return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    """Get all inventory items"""
    logger.info("Received request for all inventory")
    return jsonify({
        "items": INVENTORY_DB,
        "total_items": len(INVENTORY_DB),
        "total_in_stock": sum(1 for item in INVENTORY_DB.values() if item["available_qty"] > 0)
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Inventory Service (Beta)"})

if __name__ == '__main__':
    logger.info("Starting Inventory Service (Beta) on port 5002")
    app.run(port=5002, host='0.0.0.0')