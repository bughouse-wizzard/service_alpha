#!/usr/bin/env python3
"""
Simple integration test for Service Alpha.
Tests that the system processes orders correctly and returns 'order_status: confirmed'.
"""

import requests
import time
import threading
import sys
from flask import Flask, jsonify

# Simple mock Service Beta
def run_mock_service_beta():
    """Run a simple mock Service Beta on port 5002"""
    app = Flask(__name__)
    
    @app.route('/inventory/<item_id>', methods=['GET'])
    def inventory(item_id):
        # Always return available_qty > 0 to ensure order confirmation
        return jsonify({"available_qty": 10, "item_id": item_id})
    
    app.run(port=5002, host='0.0.0.0', debug=False, use_reloader=False)

# Import and run Service Alpha
def run_service_alpha():
    import app
    app.app.run(port=5001, host='0.0.0.0', debug=False, use_reloader=False)

def wait_for_url(url, timeout=10):
    """Wait for URL to become available"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            time.sleep(0.5)
    return False

def main():
    print("Starting integration test for Service Alpha...")
    
    # Start mock Service Beta
    print("Starting mock Service Beta on port 5002...")
    beta_thread = threading.Thread(target=run_mock_service_beta, daemon=True)
    beta_thread.start()
    
    # Wait for Service Beta
    if not wait_for_url("http://localhost:5002/inventory/test"):
        print("ERROR: Service Beta failed to start")
        return False
    print("✓ Service Beta is running")
    
    # Start Service Alpha
    print("Starting Service Alpha on port 5001...")
    alpha_thread = threading.Thread(target=run_service_alpha, daemon=True)
    alpha_thread.start()
    
    # Wait for Service Alpha (give it more time to start)
    time.sleep(3)
    
    # Test the order endpoint
    print("\nTesting /order/123 endpoint...")
    try:
        response = requests.get("http://localhost:5001/order/123", timeout=5)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('order_status') == 'confirmed':
                print("\n✓ SUCCESS: Order status is 'confirmed'!")
                print("The system correctly processes orders and returns 'order_status: confirmed'.")
                return True
            else:
                print(f"\n✗ FAILED: Expected 'order_status': 'confirmed', got: {data.get('order_status')}")
                return False
        else:
            print(f"\n✗ FAILED: Expected status 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n" + "="*60)
            print("INTEGRATION TEST PASSED!")
            print("Service Alpha correctly processes orders and returns")
            print("'order_status: confirmed' as required.")
            print("="*60)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(1)