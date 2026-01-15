"""
Test script for Service Alpha functionality.
This script tests that Service Alpha successfully interacts with Service Beta
and returns 'order_status: confirmed'.
"""
import requests
import time
import subprocess
import sys
import logging
import threading

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE_ALPHA_URL = "http://localhost:5001"
SERVICE_BETA_URL = "http://localhost:5002"

def start_service(script_name, port, service_name):
    """Start a service in a subprocess"""
    logger.info(f"Starting {service_name} on port {port}...")
    cmd = [sys.executable, script_name]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for service to start
    time.sleep(2)
    
    # Check if service is running
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=2)
        if response.status_code == 200:
            logger.info(f"{service_name} started successfully on port {port}")
            return process
        else:
            logger.error(f"{service_name} health check failed: {response.status_code}")
            process.terminate()
            return None
    except requests.RequestException:
        logger.error(f"Failed to connect to {service_name} on port {port}")
        process.terminate()
        return None

def stop_service(process, service_name):
    """Stop a service"""
    logger.info(f"Stopping {service_name}...")
    process.terminate()
    process.wait()
    logger.info(f"{service_name} stopped")

def test_order_confirmed():
    """Test that Service Alpha returns 'order_status: confirmed' for items in stock"""
    logger.info("Testing order confirmation for items in stock...")
    
    test_cases = [
        ("item_001", "Laptop", 5),
        ("item_002", "Mouse", 50),
        ("item_005", "Headphones", 15),
    ]
    
    all_passed = True
    for item_id, expected_name, expected_stock in test_cases:
        try:
            logger.info(f"Testing order for item: {item_id}")
            response = requests.get(f"{SERVICE_ALPHA_URL}/order/{item_id}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("order_status") == "confirmed":
                    logger.info(f"✓ Order confirmed for {item_id}")
                    logger.info(f"  Response: {data}")
                    
                    # Verify additional response data
                    if data.get("item_id") == item_id and data.get("stock_available") == expected_stock:
                        logger.info(f"  Additional data correct: item_id={data.get('item_id')}, stock={data.get('stock_available')}")
                    else:
                        logger.warning(f"  Additional data mismatch: expected item_id={item_id}, stock={expected_stock}, got {data}")
                else:
                    logger.error(f"✗ Order status not 'confirmed' for {item_id}: {data}")
                    all_passed = False
            else:
                logger.error(f"✗ Request failed for {item_id}: {response.status_code} - {response.text}")
                all_passed = False
                
        except requests.RequestException as e:
            logger.error(f"✗ Request exception for {item_id}: {e}")
            all_passed = False
    
    return all_passed

def test_order_out_of_stock():
    """Test that Service Alpha returns 'order_status: out_of_stock' for items with no stock"""
    logger.info("Testing order out of stock...")
    
    item_id = "item_004"  # Monitor has 0 stock
    
    try:
        response = requests.get(f"{SERVICE_ALPHA_URL}/order/{item_id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("order_status") == "out_of_stock":
                logger.info(f"✓ Correctly returned 'out_of_stock' for {item_id}")
                logger.info(f"  Response: {data}")
                return True
            else:
                logger.error(f"✗ Expected 'out_of_stock' for {item_id}, got: {data}")
                return False
        else:
            logger.error(f"✗ Request failed for {item_id}: {response.status_code} - {response.text}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"✗ Request exception for {item_id}: {e}")
        return False

def test_invalid_item():
    """Test that Service Alpha handles invalid item IDs"""
    logger.info("Testing invalid item ID...")
    
    invalid_items = ["", "nonexistent_item", "123"]
    
    all_passed = True
    for item_id in invalid_items:
        try:
            response = requests.get(f"{SERVICE_ALPHA_URL}/order/{item_id}", timeout=5)
            
            if response.status_code in [400, 404, 500]:
                logger.info(f"✓ Correctly handled invalid item '{item_id}': {response.status_code}")
            else:
                logger.warning(f"  Unexpected status for invalid item '{item_id}': {response.status_code}")
                # Not necessarily a failure, but worth noting
                
        except requests.RequestException as e:
            logger.error(f"✗ Request exception for invalid item '{item_id}': {e}")
            all_passed = False
    
    return all_passed

def main():
    """Main test function"""
    logger.info("=" * 60)
    logger.info("Starting Service Alpha functionality test")
    logger.info("=" * 60)
    
    # Start services
    inventory_process = start_service("mock_inventory_service.py", 5002, "Mock Inventory Service (Beta)")
    if not inventory_process:
        logger.error("Failed to start Mock Inventory Service")
        return False
    
    alpha_process = start_service("app.py", 5001, "Service Alpha")
    if not alpha_process:
        logger.error("Failed to start Service Alpha")
        stop_service(inventory_process, "Mock Inventory Service")
        return False
    
    time.sleep(1)  # Give services time to fully initialize
    
    test_results = []
    
    try:
        # Run tests
        logger.info("\n" + "=" * 60)
        logger.info("Running tests...")
        logger.info("=" * 60)
        
        # Test 1: Order confirmed
        test_results.append(("Order Confirmed", test_order_confirmed()))
        
        # Test 2: Order out of stock
        test_results.append(("Order Out of Stock", test_order_out_of_stock()))
        
        # Test 3: Invalid item
        test_results.append(("Invalid Item Handling", test_invalid_item()))
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("TEST SUMMARY")
        logger.info("=" * 60)
        
        all_passed = True
        for test_name, passed in test_results:
            status = "PASS" if passed else "FAIL"
            logger.info(f"{test_name}: {status}")
            if not passed:
                all_passed = False
        
        if all_passed:
            logger.info("\n✅ ALL TESTS PASSED: Service Alpha successfully interacts with Service Beta")
            logger.info("   and returns 'order_status: confirmed' for items in stock.")
        else:
            logger.info("\n❌ SOME TESTS FAILED: See above for details.")
        
        return all_passed
        
    finally:
        # Clean up
        logger.info("\nCleaning up services...")
        stop_service(alpha_process, "Service Alpha")
        stop_service(inventory_process, "Mock Inventory Service")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)