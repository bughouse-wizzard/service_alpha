#!/usr/bin/env python3
"""
Simple test to verify Service Alpha functionality.
Tests that Service Alpha returns 'order_status: confirmed' when item is in stock.
"""
import subprocess
import time
import requests
import sys
import os

def start_service(command, name, port):
    """Start a service"""
    print(f"Starting {name} on port {port}...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give it time to start
    return proc

def test_service_alpha():
    """Test Service Alpha endpoint"""
    print("\nTesting Service Alpha endpoint...")
    
    # Test with item that has stock (item_001 has stock: 5)
    try:
        response = requests.get("http://localhost:5001/order/item_001", timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('order_status') == 'confirmed':
                print("✅ SUCCESS: Service Alpha returned 'order_status: confirmed'")
                print(f"   Full response: {data}")
                return True
            else:
                print(f"❌ FAILED: Expected 'order_status: confirmed', got {data}")
                return False
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    # Kill any existing processes
    print("Cleaning up any existing processes...")
    subprocess.run('pkill -f "mock_inventory.py"', shell=True, stderr=subprocess.DEVNULL)
    subprocess.run('pkill -f "app.py"', shell=True, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    # Start mock inventory service (Service Beta)
    inventory_proc = start_service(
        "python mock_inventory.py",
        "Mock Inventory Service (Beta)",
        5002
    )
    
    # Verify Service Beta is running
    time.sleep(2)
    try:
        beta_response = requests.get("http://localhost:5002/inventory/item_001", timeout=5)
        print(f"Service Beta check: {beta_response.status_code} - {beta_response.text[:100]}")
    except:
        print("⚠️  Could not connect to Service Beta, but continuing...")
    
    # Start Service Alpha
    alpha_proc = start_service(
        "python app.py",
        "Service Alpha",
        5001
    )
    
    # Verify Service Alpha is running
    time.sleep(2)
    try:
        alpha_response = requests.get("http://localhost:5001/", timeout=5)
        print(f"Service Alpha check: {alpha_response.status_code if alpha_response else 'No response'}")
    except:
        print("⚠️  Could not connect to Service Alpha root endpoint, but continuing...")
    
    success = False
    try:
        # Run the test
        success = test_service_alpha()
        
        if success:
            print("\n" + "="*60)
            print("🎉 END-TO-END TEST PASSED!")
            print("Service Alpha successfully communicates with Service Beta")
            print("and returns 'order_status: confirmed' for items in stock.")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ END-TO-END TEST FAILED!")
            print("="*60)
            
    finally:
        # Clean up
        print("\nCleaning up processes...")
        inventory_proc.terminate()
        alpha_proc.terminate()
        inventory_proc.wait()
        alpha_proc.wait()
        print("Processes cleaned up.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)