import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration for Service Beta URL
INVENTORY_SERVICE_URL = "http://localhost:5002"

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    # Simulating a database lookup
    # In a real app, this would query a DB
    return jsonify({
        "item_id": item_id,
        "available_qty": 5  # Fixed available quantity for simplicity
    })

@app.route('/order/<item_id>', methods=['GET'])
def create_order(item_id):
    try:
        # Call Service Beta to check inventory
        response = requests.get(f"{INVENTORY_SERVICE_URL}/inventory/{item_id}")
        response.raise_for_status()
        inventory_data = response.json()
        
        # Check available quantity level
        available_qty = inventory_data.get('available_qty', 0)
        
        if available_qty > 0:
            return jsonify({"order_status": "confirmed"})
        else:
            return jsonify({"order_status": "out_of_stock"})
            
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to connect to inventory service: {str(e)}"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from inventory service"}), 500

if __name__ == '__main__':
    app.run(port=5001)
