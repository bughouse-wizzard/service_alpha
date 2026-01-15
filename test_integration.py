#!/usr/bin/env python3
"""
Integration test for Service Alpha.
Tests that Service Alpha correctly integrates with Service Beta
and handles the updated 'available_qty' field.
"""

import unittest
import json
from unittest.mock import patch, Mock
import sys
import os
import time
import threading
import requests

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestServiceAlphaIntegration(unittest.TestCase):
    """Test suite for Service Alpha integration with Service Beta"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('app.requests.get')
    def test_order_confirmed_when_available_qty_present(self, mock_get):
        """Test that Service Alpha correctly interprets 'available_qty' field from Service Beta"""
        # Mock Service Beta response with 'available_qty' field
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available_qty": 5}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/test_item_123')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')
        
        # Verify Service Beta was called with correct URL
        mock_get.assert_called_once_with("http://localhost:5002/inventory/test_item_123")
    
    @patch('app.requests.get')
    def test_order_out_of_stock_when_available_qty_zero(self, mock_get):
        """Test that Service Alpha returns out_of_stock when available_qty is 0"""
        # Mock Service Beta response with zero available_qty
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available_qty": 0}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/test_item_456')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'out_of_stock')
        
        # Verify Service Beta was called with correct URL
        mock_get.assert_called_once_with("http://localhost:5002/inventory/test_item_456")
    
    @patch('app.requests.get')
    def test_backward_compatibility_with_stock_field(self, mock_get):
        """Test that Service Alpha still works with old 'stock' field for backward compatibility"""
        # Mock Service Beta response with old 'stock' field (no 'available_qty')
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stock": 3}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/legacy_item_789')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')
        
        # Verify Service Beta was called with correct URL
        mock_get.assert_called_once_with("http://localhost:5002/inventory/legacy_item_789")
    
    @patch('app.requests.get')
    def test_order_out_of_stock_when_stock_zero(self, mock_get):
        """Test that Service Alpha returns out_of_stock when stock is 0 (backward compatibility)"""
        # Mock Service Beta response with zero stock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stock": 0}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/legacy_item_999')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'out_of_stock')
    
    @patch('app.requests.get')
    def test_error_handling_when_service_beta_unavailable(self, mock_get):
        """Test that Service Alpha handles errors when Service Beta is unavailable"""
        # Mock Service Beta connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Make request to Service Alpha
        response = self.app.get('/order/test_item_error')
        
        # Verify error response
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Failed to connect to inventory service', data['error'])
    
    @patch('app.requests.get')
    def test_error_handling_when_invalid_json_response(self, mock_get):
        """Test that Service Alpha handles invalid JSON responses from Service Beta"""
        # Mock Service Beta response with invalid JSON
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/test_item_invalid')
        
        # Verify error response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid response from inventory service')
    
    @patch('app.requests.get')
    def test_available_qty_takes_precedence_over_stock(self, mock_get):
        """Test that 'available_qty' field takes precedence over 'stock' field when both are present"""
        # Mock Service Beta response with both fields
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available_qty": 10, "stock": 0}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/item_with_both_fields')
        
        # Verify response - should use available_qty (10) not stock (0)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')


def run_service_alpha():
    """Helper function to run Service Alpha in a thread for integration testing"""
    app.run(port=5001, debug=False, use_reloader=False)


class LiveIntegrationTest(unittest.TestCase):
    """Live integration tests with actual Service Alpha server"""
    
    @classmethod
    def setUpClass(cls):
        """Start Service Alpha server before running tests"""
        cls.server_thread = threading.Thread(target=run_service_alpha, daemon=True)
        cls.server_thread.start()
        # Give server time to start
        time.sleep(2)
    
    def test_live_service_alpha_endpoint(self):
        """Test that Service Alpha server is running and responding"""
        try:
            response = requests.get('http://localhost:5001/order/test', timeout=5)
            # We expect an error since Service Beta is not running
            # But at least the server should respond
            self.assertIn(response.status_code, [503, 500])
        except requests.exceptions.ConnectionError:
            self.fail("Service Alpha server is not running")


if __name__ == '__main__':
    print("Running Service Alpha integration tests...")
    print("=" * 60)
    
    # Run unit tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestServiceAlphaIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    unit_test_result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("Unit tests completed.")
    
    # Only run live tests if unit tests passed
    if unit_test_result.wasSuccessful():
        print("\nRunning live integration tests...")
        print("=" * 60)
        
        live_suite = loader.loadTestsFromTestCase(LiveIntegrationTest)
        live_result = runner.run(live_suite)
        
        if live_result.wasSuccessful():
            print("\n" + "=" * 60)
            print("✅ All tests passed! Service Alpha integration is working correctly.")
            print("The system correctly handles the updated 'available_qty' field.")
        else:
            print("\n" + "=" * 60)
            print("❌ Live integration tests failed.")
    else:
        print("\n" + "=" * 60)
        print("❌ Unit tests failed. Skipping live integration tests.")