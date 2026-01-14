import unittest
import json
from unittest.mock import patch, Mock
import sys
import os

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestServiceAlphaIntegration(unittest.TestCase):
    
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
        response = self.app.get('/order/123')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')
        
        # Verify Service Beta was called with correct URL
        mock_get.assert_called_once_with("http://localhost:5002/inventory/123")
    
    @patch('app.requests.get')
    def test_order_out_of_stock_when_available_qty_zero(self, mock_get):
        """Test that Service Alpha returns out_of_stock when available_qty is 0"""
        # Mock Service Beta response with zero available_qty
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available_qty": 0}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/456')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'out_of_stock')
    
    @patch('app.requests.get')
    def test_order_confirmed_when_stock_field_present(self, mock_get):
        """Test backward compatibility with 'stock' field"""
        # Mock Service Beta response with 'stock' field (backward compatibility)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stock": 3}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/789')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')
    
    @patch('app.requests.get')
    def test_order_out_of_stock_when_stock_zero(self, mock_get):
        """Test backward compatibility with zero stock"""
        # Mock Service Beta response with zero stock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stock": 0}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/999')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'out_of_stock')
    
    @patch('app.requests.get')
    def test_prefers_available_qty_over_stock(self, mock_get):
        """Test that available_qty takes precedence over stock when both fields are present"""
        # Mock Service Beta response with both fields
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stock": 0, "available_qty": 5}
        mock_get.return_value = mock_response
        
        # Make request to Service Alpha
        response = self.app.get('/order/111')
        
        # Verify response should be confirmed (available_qty > 0)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['order_status'], 'confirmed')
    
    @patch('app.requests.get')
    def test_service_beta_connection_error(self, mock_get):
        """Test handling of Service Beta connection errors"""
        # Mock connection error
        mock_get.side_effect = Exception("Connection failed")
        
        # Make request to Service Alpha
        response = self.app.get('/order/222')
        
        # Verify error response
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Failed to connect', data['error'])

if __name__ == '__main__':
    unittest.main()