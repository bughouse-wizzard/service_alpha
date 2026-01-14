#!/usr/bin/env python3
"""
Test edge cases for Service Alpha to ensure comprehensive testing.
"""

import subprocess
import time
import requests
import json
import sys
import os

def test_out_of_stock():
    """Test that Service Alpha returns 'out_of_stock' when inventory has 0 stock"""
    print("Testing out_of_stock scenario...")
    
    # Create mock inventory service that returns 0 stock
    mock_code = """
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    # Return 0 stock to trigger 'out_of_stock' status
    return jsonify({"stock": 0, "item_id": item_id})

if __name__ == '__main__':
    app.run(port=5002, debug=False)
"""
    
    with open("mock_inventory_zero.py", "w") as f:
        f.write(mock_code)
    
    # Start mock inventory service
    inventory_proc = subprocess.Popen(
        [sys.executable, "mock_inventory_zero.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Start Service Alpha
    alpha_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        time.sleep(3)
        
        # Make request
        response = requests.get("http://localhost:5001/order/out-of-stock-item", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get("order_status") == "out_of_stock":
            print("✓ SUCCESS: Correctly returns 'out_of_stock' when inventory is 0")
            return True
        else:
            print(f"✗ FAIL: Expected 'out_of_stock', got '{data.get('order_status')}'")
            return False
            
    finally:
        alpha_proc.terminate()
        inventory_proc.terminate()
        alpha_proc.wait()
        inventory_proc.wait()
        
        if os.path.exists("mock_inventory_zero.py"):
            os.remove("mock_inventory_zero.py")

def test_inventory_service_error():
    """Test that Service Alpha handles inventory service errors gracefully"""
    print("\nTesting inventory service error scenario...")
    
    # Start Service Alpha without inventory service
    alpha_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        time.sleep(2)
        
        # Make request - inventory service should not be running
        response = requests.get("http://localhost:5001/order/any-item", timeout=5)
        
        print(f"Status code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 503 and "error" in data:
            print("✓ SUCCESS: Correctly handles inventory service errors")
            return True
        else:
            print("✗ FAIL: Did not handle inventory service error as expected")
            return False
            
    finally:
        alpha_proc.terminate()
        alpha_proc.wait()

def main():
    """Run comprehensive edge case tests"""
    print("=" * 60)
    print("Service Alpha Edge Case Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: out_of_stock scenario
    if not test_out_of_stock():
        all_passed = False
    
    # Test 2: inventory service error
    if not test_inventory_service_error():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL EDGE CASE TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())