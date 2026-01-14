#!/usr/bin/env python3
"""
Test script to verify Service Alpha response includes 'order_status: confirmed'
This script starts Service Alpha and a mock inventory service, then makes a test request.
"""

import subprocess
import time
import requests
import json
import sys
import os
from threading import Thread

def start_service_alpha():
    """Start Service Alpha in a subprocess"""
    print("Starting Service Alpha...")
    # Use the existing app.py
    return subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def start_mock_inventory_service():
    """Start a simple mock inventory service that returns stock > 0"""
    print("Starting mock inventory service...")
    
    mock_code = """
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    # Always return stock > 0 to trigger 'confirmed' status
    return jsonify({"stock": 5, "item_id": item_id})

if __name__ == '__main__':
    app.run(port=5002, debug=False)
"""
    
    # Write mock service to a temporary file
    with open("mock_inventory.py", "w") as f:
        f.write(mock_code)
    
    return subprocess.Popen(
        [sys.executable, "mock_inventory.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def test_service_alpha():
    """Make a request to Service Alpha and verify response"""
    print("Testing Service Alpha...")
    
    # Give services time to start
    time.sleep(2)
    
    try:
        # Make request to Service Alpha
        response = requests.get("http://localhost:5001/order/test-item-123", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"Response received: {json.dumps(data, indent=2)}")
        
        # Check if response contains 'order_status: confirmed'
        if "order_status" in data:
            if data["order_status"] == "confirmed":
                print("✓ SUCCESS: Response includes 'order_status: confirmed'")
                return True
            else:
                print(f"✗ FAIL: Response has 'order_status' but value is '{data['order_status']}', not 'confirmed'")
                return False
        else:
            print("✗ FAIL: Response does not contain 'order_status' field")
            print(f"  Available fields: {list(data.keys())}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ FAIL: Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ FAIL: Invalid JSON response: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Service Alpha Integration Test")
    print("Verifying response includes 'order_status: confirmed'")
    print("=" * 60)
    
    # Start services
    alpha_proc = start_service_alpha()
    inventory_proc = start_mock_inventory_service()
    
    try:
        # Wait a bit for services to start
        time.sleep(3)
        
        # Run test
        success = test_service_alpha()
        
        if success:
            print("\n" + "=" * 60)
            print("TEST PASSED: Service Alpha correctly returns 'order_status: confirmed'")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("TEST FAILED: Service Alpha does not return expected response")
            print("=" * 60)
            return 1
            
    finally:
        # Clean up
        print("\nCleaning up services...")
        alpha_proc.terminate()
        inventory_proc.terminate()
        alpha_proc.wait()
        inventory_proc.wait()
        
        # Clean up temporary files
        if os.path.exists("mock_inventory.py"):
            os.remove("mock_inventory.py")
        
        # Print service logs for debugging
        print("\nService Alpha stdout:")
        print(alpha_proc.stdout.read() if alpha_proc.stdout else "No output")
        print("\nService Alpha stderr:")
        print(alpha_proc.stderr.read() if alpha_proc.stderr else "No output")
        
        print("\nMock Inventory stdout:")
        print(inventory_proc.stdout.read() if inventory_proc.stdout else "No output")
        print("\nMock Inventory stderr:")
        print(inventory_proc.stderr.read() if inventory_proc.stderr else "No output")

if __name__ == "__main__":
    sys.exit(main())