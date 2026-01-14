import requests
from flask import Flask, jsonify
import map_maker

app = Flask(__name__)

# Configuration for Service Beta URL
INVENTORY_SERVICE_URL = "http://localhost:5002"

@app.route('/order/<item_id>', methods=['GET'])
def create_order(item_id):
    try:
        # Call Service Beta to check inventory
        response = requests.get(f"{INVENTORY_SERVICE_URL}/inventory/{item_id}")
        response.raise_for_status()
        inventory_data = response.json()
        
        # Use map_maker to process inventory data and ensure available_qty is correctly handled
        mapped_data = map_maker.map_inventory_data(inventory_data)
        available_qty = mapped_data.get('available_qty', 0)
        
        # Validate available_qty
        if not map_maker.validate_available_qty(available_qty):
            return jsonify({"error": "Invalid available_qty value received from inventory service"}), 500
        
        if available_qty > 0:
            # Create order payload using map_maker
            order_payload = map_maker.create_order_payload(item_id, available_qty)
            return jsonify({
                "order_status": "confirmed",
                "order_details": order_payload
            })
        else:
            return jsonify({"order_status": "out_of_available_qty"})
            
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to connect to inventory service: {str(e)}"}), 503
    except ValueError:
        return jsonify({"error": "Invalid response from inventory service"}), 500

if __name__ == '__main__':
    app.run(port=5001)
