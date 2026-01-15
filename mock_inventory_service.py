"""
Mock Service Beta (Inventory Service) for testing Service Alpha.
This service runs on port 5002 and provides inventory data.
"""
from flask import Flask, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock inventory database
INVENTORY_DB = {
    "item_001": {"name": "Laptop", "stock": 5, "price": 999.99},
    "item_002": {"name": "Mouse", "stock": 50, "price": 29.99},
    "item_003": {"name": "Keyboard", "stock": 25, "price": 79.99},
    "item_004": {"name": "Monitor", "stock": 0, "price": 299.99},  # Out of stock
    "item_005": {"name": "Headphones", "stock": 15, "price": 149.99},
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
            "stock": item_data["stock"],
            "price": item_data["price"],
            "in_stock": item_data["stock"] > 0
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
        "total_in_stock": sum(1 for item in INVENTORY_DB.values() if item["stock"] > 0)
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Mock Inventory Service"})

if __name__ == '__main__':
    logger.info("Starting Mock Inventory Service on port 5002")
    app.run(port=5002, host='0.0.0.0')