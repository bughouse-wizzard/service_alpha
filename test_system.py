import subprocess
import time
import requests
import sys
import os

def start_service(script_name, port, log_file):
    """Start a Flask service"""
    print(f"Starting {script_name} on port {port}...")
    with open(log_file, 'w') as f:
        proc = subprocess.Popen(
            [sys.executable, script_name],
            stdout=f,
            stderr=subprocess.STDOUT
        )
    time.sleep(3)  # Give it time to start
    return proc

def test_service_alpha():
    """Test Service Alpha endpoint"""
    print("\nTesting Service Alpha...")
    
    # Test with item that has stock
    response = requests.get("http://localhost:5001/order/item_001")
    print(f"Response for item_001: {response.status_code} - {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('order_status') == 'confirmed':
            print("✓ SUCCESS: Received 'order_status: confirmed'")
            return True
        else:
            print(f"✗ FAILED: Expected 'order_status: confirmed', got {data}")
            return False
    else:
        print(f"✗ FAILED: HTTP {response.status_code}")
        return False

def main():
    # Kill any existing processes
    subprocess.run(['pkill', '-f', 'mock_inventory'], stderr=subprocess.DEVNULL)
    subprocess.run(['pkill', '-f', 'app.py'], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # Start mock inventory service
    inventory_proc = start_service("mock_inventory.py", 5002, "inventory_test.log")
    
    # Start Service Alpha
    service_alpha_proc = start_service("app.py", 5001, "service_alpha_test.log")
    
    try:
        # Test the system
        success = test_service_alpha()
        
        if success:
            print("\n" + "="*50)
            print("SYSTEM TEST PASSED!")
            print("Service Alpha correctly communicates with Service Beta")
            print("and returns 'order_status: confirmed'")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("SYSTEM TEST FAILED!")
            print("="*50)
            sys.exit(1)
            
    finally:
        # Clean up
        print("\nCleaning up processes...")
        inventory_proc.terminate()
        service_alpha_proc.terminate()
        inventory_proc.wait()
        service_alpha_proc.wait()

if __name__ == "__main__":
    main()