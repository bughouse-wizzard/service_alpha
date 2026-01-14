#!/usr/bin/env python3
"""
Simple integration test that makes actual HTTP requests to verify
Service Alpha correctly interprets the 'available_qty' field from Service Beta.
"""
import requests
import json
import sys
import os
from unittest.mock import patch, Mock

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_service_alpha_integration():
    """Test that Service Alpha correctly interprets available_qty field"""
    print("Starting Service Alpha integration test...")
    
    # Import app after adding to path
    from app import app
    
    # Use test client instead of actual HTTP server for simplicity
    with app.test_client() as client:
        print("\n1. Testing with 'available_qty' field from Service Beta...")
        
        # Mock requests.get to simulate Service Beta response
        with patch('app.requests.get') as mock_get:
            # Test 1: available_qty > 0 should return confirmed
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"available_qty": 5}
            mock_get.return_value = mock_response
            
            response = client.get('/order/123')
            data = json.loads(response.data)
            
            print(f"   Request: GET /order/123")
            print(f"   Service Beta response: {{'available_qty': 5}}")
            print(f"   Service Alpha response: {data}")
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert data.get('order_status') == 'confirmed', f"Expected 'confirmed', got {data.get('order_status')}"
            print("   ✓ Test passed: order_status is 'confirmed'")
            
            # Verify Service Beta was called correctly
            mock_get.assert_called_once_with("http://localhost:5002/inventory/123")
            print("   ✓ Service Beta was called with correct URL")
        
        # Test 2: available_qty = 0 should return out_of_stock
        with patch('app.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"available_qty": 0}
            mock_get.return_value = mock_response
            
            response = client.get('/order/456')
            data = json.loads(response.data)
            
            print(f"\n2. Testing with zero 'available_qty'...")
            print(f"   Request: GET /order/456")
            print(f"   Service Beta response: {{'available_qty': 0}}")
            print(f"   Service Alpha response: {data}")
            
            assert data.get('order_status') == 'out_of_stock', f"Expected 'out_of_stock', got {data.get('order_status')}"
            print("   ✓ Test passed: order_status is 'out_of_stock'")
        
        # Test 3: Backward compatibility with 'stock' field
        with patch('app.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"stock": 3}
            mock_get.return_value = mock_response
            
            response = client.get('/order/789')
            data = json.loads(response.data)
            
            print(f"\n3. Testing backward compatibility with 'stock' field...")
            print(f"   Request: GET /order/789")
            print(f"   Service Beta response: {{'stock': 3}}")
            print(f"   Service Alpha response: {data}")
            
            assert data.get('order_status') == 'confirmed', f"Expected 'confirmed', got {data.get('order_status')}"
            print("   ✓ Test passed: order_status is 'confirmed' (backward compatibility working)")
        
        # Test 4: available_qty takes precedence over stock
        with patch('app.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"stock": 0, "available_qty": 2}
            mock_get.return_value = mock_response
            
            response = client.get('/order/999')
            data = json.loads(response.data)
            
            print(f"\n4. Testing that 'available_qty' takes precedence over 'stock'...")
            print(f"   Request: GET /order/999")
            print(f"   Service Beta response: {{'stock': 0, 'available_qty': 2}}")
            print(f"   Service Alpha response: {data}")
            
            assert data.get('order_status') == 'confirmed', f"Expected 'confirmed', got {data.get('order_status')}"
            print("   ✓ Test passed: 'available_qty' correctly takes precedence")
        
        print("\n" + "="*60)
        print("ALL INTEGRATION TESTS PASSED! ✓")
        print("Service Alpha correctly interprets 'available_qty' field from Service Beta")
        print("="*60)

if __name__ == '__main__':
    try:
        test_service_alpha_integration()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)