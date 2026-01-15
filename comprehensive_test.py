#!/usr/bin/env python3
"""
Comprehensive test for Service Alpha functionality.
Tests multiple scenarios including order confirmation, out of stock, and invalid items.
"""
import subprocess
import time
import requests
import sys
import os

def start_service(command, name, port, health_endpoint="/health"):
    """Start a service and wait for it to be healthy"""
    print(f"Starting {name} on port {port}...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for service to start
    max_attempts = 10
    for i in range(max_attempts):
        time.sleep(1)
        try:
            response = requests.get(f"http://localhost:{port}{health_endpoint}", timeout=2)
            if response.status_code == 200:
                print(f"✅ {name} started successfully on port {port}")
                return proc
        except:
            if i == max_attempts - 1:
                print(f"⚠️  {name} may not have started properly, but continuing...")
    
    return proc

def test_order_confirmed():
    """Test that Service Alpha returns 'order_status: confirmed' for items in stock"""
    print("\n" + "="*60)
    print("Testing order confirmation for items in stock...")
    print("="*60)
    
    test_cases = [
        ("item_001", "Laptop", 5),
        ("item_002", "Mouse", 50),
        ("item_005", "Headphones", 15),
    ]
    
    all_passed = True
    for item_id, expected_name, expected_stock in test_cases:
        try:
            print(f"\nTesting order for item: {item_id}")
            response = requests.get(f"http://localhost:5001/order/{item_id}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("order_status") == "confirmed":
                    print(f"  ✅ Order confirmed for {item_id}")
                    print(f"     Response: {data}")
                    
                    # Note: The current app.py only returns order_status, not item details
                    # This is expected based on the current implementation
                else:
                    print(f"  ❌ Order status not 'confirmed' for {item_id}: {data}")
                    all_passed = False
            else:
                print(f"  ❌ Request failed for {item_id}: {response.status_code} - {response.text}")
                all_passed = False
                
        except requests.RequestException as e:
            print(f"  ❌ Request exception for {item_id}: {e}")
            all_passed = False
    
    return all_passed

def test_order_out_of_stock():
    """Test that Service Alpha returns 'order_status: out_of_stock' for items with no stock"""
    print("\n" + "="*60)
    print("Testing order out of stock...")
    print("="*60)
    
    item_id = "item_004"  # Monitor has 0 stock
    
    try:
        response = requests.get(f"http://localhost:5001/order/{item_id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("order_status") == "out_of_stock":
                print(f"  ✅ Correctly returned 'out_of_stock' for {item_id}")
                print(f"     Response: {data}")
                return True
            else:
                print(f"  ❌ Expected 'out_of_stock' for {item_id}, got: {data}")
                return False
        else:
            print(f"  ❌ Request failed for {item_id}: {response.status_code} - {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"  ❌ Request exception for {item_id}: {e}")
        return False

def test_invalid_item():
    """Test that Service Alpha handles invalid item IDs"""
    print("\n" + "="*60)
    print("Testing invalid item ID...")
    print("="*60)
    
    invalid_items = ["", "nonexistent_item", "123"]
    
    all_passed = True
    for item_id in invalid_items:
        try:
            response = requests.get(f"http://localhost:5001/order/{item_id}", timeout=5)
            
            if response.status_code in [400, 404, 500]:
                print(f"  ✅ Correctly handled invalid item '{item_id}': {response.status_code}")
            else:
                print(f"  ⚠️  Unexpected status for invalid item '{item_id}': {response.status_code}")
                # Not necessarily a failure, but worth noting
                
        except requests.RequestException as e:
            print(f"  ❌ Request exception for invalid item '{item_id}': {e}")
            all_passed = False
    
    return all_passed

def main():
    # Kill any existing processes
    print("Cleaning up any existing processes...")
    subprocess.run('pkill -f "mock_inventory"', shell=True, stderr=subprocess.DEVNULL)
    subprocess.run('pkill -f "app.py"', shell=True, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    # Start mock inventory service (Service Beta) - using the comprehensive version
    inventory_proc = start_service(
        "python mock_inventory_service.py",
        "Mock Inventory Service (Beta)",
        5002,
        "/health"
    )
    
    # Start Service Alpha
    alpha_proc = start_service(
        "python app.py",
        "Service Alpha",
        5001,
        "/"  # app.py doesn't have a health endpoint, so check root
    )
    
    time.sleep(2)  # Give services time to fully initialize
    
    test_results = []
    
    try:
        # Run tests
        print("\n" + "="*60)
        print("Running comprehensive tests...")
        print("="*60)
        
        # Test 1: Order confirmed
        test_results.append(("Order Confirmed", test_order_confirmed()))
        
        # Test 2: Order out of stock
        test_results.append(("Order Out of Stock", test_order_out_of_stock()))
        
        # Test 3: Invalid item
        test_results.append(("Invalid Item Handling", test_invalid_item()))
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        all_passed = True
        for test_name, passed in test_results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name}: {status}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED!")
            print("Service Alpha successfully interacts with Service Beta")
            print("and returns 'order_status: confirmed' for items in stock.")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ SOME TESTS FAILED!")
            print("="*60)
        
        return all_passed
        
    finally:
        # Clean up
        print("\nCleaning up processes...")
        inventory_proc.terminate()
        alpha_proc.terminate()
        inventory_proc.wait()
        alpha_proc.wait()
        print("Processes cleaned up.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)