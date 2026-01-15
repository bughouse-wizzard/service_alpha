from flask import Flask, jsonify

app = Flask(__name__)

# Mock inventory data
inventory = {
    "item_001": {"stock": 5, "name": "Widget A"},
    "item_002": {"stock": 0, "name": "Widget B"},
    "item_003": {"stock": 10, "name": "Widget C"},
    "item_123": {"stock": 3, "name": "Test Item"}
}

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    if item_id in inventory:
        return jsonify(inventory[item_id])
    else:
        # Default item with stock for testing
        return jsonify({"stock": 1, "name": "Default Item"})

if __name__ == '__main__':
    app.run(port=5002, debug=True)