"""
Tests for LLM Engine functionality.
"""

import json
import os
import tempfile
from unittest.mock import Mock, patch
import pytest

from app.services.llm_engine import LLMEngine


class TestLLMEngine:
    """Test suite for LLMEngine class."""
    
    def setup_method(self):
        """Setup test environment."""
        # Create a temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock settings
        self.mock_settings = Mock()
        self.mock_settings.DEEPSEEK_API_KEY = "test-api-key"
        self.mock_settings.DEEPSEEK_BASE_URL = "https://api.deepseek.com"
        self.mock_settings.DEEPSEEK_MODEL = "deepseek-chat"
        self.mock_settings.DEEPSEEK_TEMPERATURE = 0.1
        self.mock_settings.DEEPSEEK_MAX_TOKENS = 4000
        
        # Patch settings
        self.settings_patcher = patch('app.services.llm_engine.settings', self.mock_settings)
        self.settings_patcher.start()
        
        # Create LLMEngine instance
        self.engine = LLMEngine()
        
        # Mock the OpenAI client
        self.engine.client = Mock()
    
    def teardown_method(self):
        """Cleanup after tests."""
        self.settings_patcher.stop()
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test LLMEngine initialization."""
        assert self.engine.model == "deepseek-chat"
        assert self.engine.temperature == 0.1
        assert self.engine.max_tokens == 4000
        assert self.engine.client is not None
    
    def test_log_interaction(self):
        """Test logging of LLM interactions."""
        # Create a temporary log directory
        log_dir = os.path.join(self.temp_dir, "logs", "llm")
        self.engine.log_dir = log_dir
        
        prompt = "Test prompt"
        response = "Test response"
        function_name = "test_function"
        
        # Call _log_interaction
        self.engine._log_interaction(prompt, response, function_name)
        
        # Check that log directory was created
        assert os.path.exists(log_dir)
        
        # Check that a log file was created
        log_files = os.listdir(log_dir)
        assert len(log_files) == 1
        assert function_name in log_files[0]
        
        # Check log content
        log_file = os.path.join(log_dir, log_files[0])
        with open(log_file, 'r') as f:
            content = f.read()
            assert prompt in content
            assert response in content
            assert function_name in content
    
    def test_call_llm_json_mode(self):
        """Test calling LLM with JSON mode."""
        # Mock response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = '{"test": "value"}'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_response
        
        # Call _call_llm with json_mode=True
        result = self.engine._call_llm("Test prompt", json_mode=True)
        
        # Verify the call
        self.engine.client.chat.completions.create.assert_called_once()
        call_args = self.engine.client.chat.completions.create.call_args
        
        # Check that response_format was set for JSON
        assert call_args[1]['response_format'] == {"type": "json_object"}
        assert result == '{"test": "value"}'
    
    def test_call_llm_without_json_mode(self):
        """Test calling LLM without JSON mode."""
        # Mock response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Plain text response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_response
        
        # Call _call_llm with json_mode=False
        result = self.engine._call_llm("Test prompt", json_mode=False)
        
        # Verify the call
        self.engine.client.chat.completions.create.assert_called_once()
        call_args = self.engine.client.chat.completions.create.call_args
        
        # Check that response_format was None (not JSON object)
        assert call_args[1]['response_format'] is None
        assert result == "Plain text response"
    
    def test_extract_specs_success(self):
        """Test successful extraction of specifications."""
        # Mock LLM response
        mock_response = {
            "product_name": "Test Product",
            "manufacturer": "Test Manufacturer",
            "model": "XYZ-123",
            "technical_specs": {
                "weight": "10kg",
                "dimensions": "100x50x30cm"
            },
            "quantity": 5,
            "unit_price": 100.0,
            "total_price": 500.0,
            "delivery_terms": "30 days",
            "warranty": "2 years"
        }
        
        mock_llm_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(mock_response)
        mock_choice.message = mock_message
        mock_llm_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_llm_response
        
        # Test text
        test_text = "Test product specifications: Product XYZ-123 from Test Manufacturer, weight 10kg, dimensions 100x50x30cm"
        test_ktru = "123456"
        
        # Call extract_specs
        result = self.engine.extract_specs(test_text, test_ktru)
        
        # Verify result
        assert result["product_name"] == "Test Product"
        assert result["manufacturer"] == "Test Manufacturer"
        assert result["model"] == "XYZ-123"
        assert result["technical_specs"]["weight"] == "10kg"
        assert result["technical_specs"]["dimensions"] == "100x50x30cm"
        assert result["quantity"] == 5
        assert result["unit_price"] == 100.0
        assert result["total_price"] == 500.0
        assert result["delivery_terms"] == "30 days"
        assert result["warranty"] == "2 years"
        assert result["ktru_code"] == "123456"
        assert "extraction_timestamp" in result
    
    def test_extract_specs_json_error(self):
        """Test extraction with invalid JSON response."""
        # Mock LLM response with invalid JSON
        mock_llm_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Invalid JSON response"
        mock_choice.message = mock_message
        mock_llm_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_llm_response
        
        # Test text
        test_text = "Test product"
        
        # Call extract_specs - should raise ValueError
        with pytest.raises(ValueError, match="Invalid JSON response from LLM"):
            self.engine.extract_specs(test_text)
    
    def test_compare_specs_success(self):
        """Test successful comparison of specifications."""
        # Mock LLM response
        mock_response = {
            "overall_match_score": 0.95,
            "manufacturer_match": True,
            "model_match": True,
            "technical_comparison": {
                "weight": {
                    "target_value": "10kg",
                    "contract_value": "10kg",
                    "match": True,
                    "notes": "Exact match"
                },
                "dimensions": {
                    "target_value": "100x50x30cm",
                    "contract_value": "100x50x30cm",
                    "match": True,
                    "notes": "Exact match"
                }
            },
            "critical_mismatches": [],
            "recommendation": "Good match",
            "compatibility_assessment": "Fully compatible"
        }
        
        mock_llm_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(mock_response)
        mock_choice.message = mock_message
        mock_llm_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_llm_response
        
        # Test data
        target_specs = {
            "product_name": "Product A",
            "manufacturer": "Manufacturer X",
            "model": "XYZ-123",
            "technical_specs": {
                "weight": "10kg",
                "dimensions": "100x50x30cm"
            }
        }
        
        contract_specs = {
            "product_name": "Product A",
            "manufacturer": "Manufacturer X",
            "model": "XYZ-123",
            "technical_specs": {
                "weight": "10kg",
                "dimensions": "100x50x30cm"
            }
        }
        
        # Call compare_specs
        result = self.engine.compare_specs(target_specs, contract_specs)
        
        # Verify result
        assert result["overall_match_score"] == 0.95
        assert result["manufacturer_match"] is True
        assert result["model_match"] is True
        assert result["technical_comparison"]["weight"]["match"] is True
        assert result["technical_comparison"]["dimensions"]["match"] is True
        assert result["critical_mismatches"] == []
        assert result["recommendation"] == "Good match"
        assert result["compatibility_assessment"] == "Fully compatible"
        assert result["target_product"] == "Product A"
        assert result["contract_product"] == "Product A"
        assert "comparison_timestamp" in result
    
    def test_compare_specs_with_mismatches(self):
        """Test comparison with mismatches."""
        # Mock LLM response with mismatches
        mock_response = {
            "overall_match_score": 0.65,
            "manufacturer_match": True,
            "model_match": False,
            "technical_comparison": {
                "weight": {
                    "target_value": "10kg",
                    "contract_value": "12kg",
                    "match": False,
                    "notes": "Weight differs by 2kg"
                }
            },
            "critical_mismatches": ["model"],
            "recommendation": "Partial match with significant differences",
            "compatibility_assessment": "May require verification"
        }
        
        mock_llm_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(mock_response)
        mock_choice.message = mock_message
        mock_llm_response.choices = [mock_choice]
        
        self.engine.client.chat.completions.create.return_value = mock_llm_response
        
        # Test data with mismatches
        target_specs = {
            "product_name": "Product A",
            "manufacturer": "Manufacturer X",
            "model": "XYZ-123",
            "technical_specs": {"weight": "10kg"}
        }
        
        contract_specs = {
            "product_name": "Product B",
            "manufacturer": "Manufacturer X",
            "model": "XYZ-456",
            "technical_specs": {"weight": "12kg"}
        }
        
        # Call compare_specs
        result = self.engine.compare_specs(target_specs, contract_specs)
        
        # Verify result shows mismatches
        assert result["overall_match_score"] == 0.65
        assert result["manufacturer_match"] is True
        assert result["model_match"] is False
        assert result["technical_comparison"]["weight"]["match"] is False
        assert "model" in result["critical_mismatches"]
        assert "Partial match" in result["recommendation"]
    
    def test_batch_extract_specs(self):
        """Test batch extraction of specifications."""
        # Mock responses for batch
        mock_responses = [
            json.dumps({
                "product_name": f"Product {i}",
                "manufacturer": f"Manufacturer {i}",
                "model": f"MODEL-{i}"
            }) for i in range(3)
        ]
        
        # Setup mock to return different responses
        self.engine.client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content=mock_responses[i]))]) for i in range(3)
        ]
        
        # Test texts
        texts = ["Text 1", "Text 2", "Text 3"]
        ktru_codes = ["KTRU001", "KTRU002", "KTRU003"]
        
        # Call batch_extract_specs
        results = self.engine.batch_extract_specs(texts, ktru_codes)
        
        # Verify results
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["product_name"] == f"Product {i}"
            assert result["manufacturer"] == f"Manufacturer {i}"
            assert result["model"] == f"MODEL-{i}"
            assert result["ktru_code"] == f"KTRU00{i+1}"
    
    def test_batch_extract_specs_with_error(self):
        """Test batch extraction with one failing item."""
        # Mock responses - second one will fail
        mock_responses = [
            json.dumps({"product_name": "Product 1"}),
            "Invalid JSON",  # This will cause JSONDecodeError
            json.dumps({"product_name": "Product 3"})
        ]
        
        # Setup mock to return different responses
        self.engine.client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content=mock_responses[i]))]) for i in range(3)
        ]
        
        # Test texts
        texts = ["Text 1", "Text 2", "Text 3"]
        
        # Call batch_extract_specs
        results = self.engine.batch_extract_specs(texts)
        
        # Verify results - second item should have error
        assert len(results) == 3
        assert "product_name" in results[0]
        assert "error" in results[1]
        assert "product_name" in results[2]
        assert results[1]["text_index"] == 1
    
    def test_batch_extract_specs_invalid_input(self):
        """Test batch extraction with invalid input (mismatched lengths)."""
        texts = ["Text 1", "Text 2"]
        ktru_codes = ["KTRU001"]  # Only one code for two texts
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Number of texts must match number of KTRU codes"):
            self.engine.batch_extract_specs(texts, ktru_codes)