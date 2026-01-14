from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    # Simulating a database lookup
    # In a real app, this would query a DB
    return jsonify({
        "item_id": item_id,
        "available_qty": 5  # Fixed available quantity for simplicity
    })

if __name__ == '__main__':
    app.run(port=5002)