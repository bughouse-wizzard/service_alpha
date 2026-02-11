"""
Tests for DeepSeek AI client wrapper.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
import os

from app.services.ai.client import DeepSeekClient, DeepSeekClientConfig
from openai import APIConnectionError, APIError, RateLimitError


# Create exception classes for testing that inherit from OpenAI exceptions
class MockAPIError(APIError):
    def __init__(self, status_code=500, message="Internal Server Error"):
        self.status_code = status_code
        self.message = message
        # Create a mock request object
        mock_request = Mock()
        mock_request.method = "POST"
        mock_request.url = "https://api.deepseek.com/v1/chat/completions"
        super().__init__(message=message, request=mock_request, body=None)


class MockAPIConnectionError(APIConnectionError):
    def __init__(self, message="Connection failed"):
        self.message = message
        # Create a mock request object
        mock_request = Mock()
        mock_request.method = "POST"
        mock_request.url = "https://api.deepseek.com/v1/chat/completions"
        super().__init__(message=message, request=mock_request)


class TestDeepSeekClient:
    """Test suite for DeepSeekClient."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variable for API key
        os.environ["DEEPSEEK_API_KEY"] = "test-api-key-123"
        
        # Create test config
        self.config = DeepSeekClientConfig(
            api_key="test-api-key-123",
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            timeout=5,
            max_retries=2,
            retry_delay=0.1
        )
        
        # Test messages
        self.test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
        
        # Test JSON schema
        self.test_json_schema = {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "confidence": {"type": "number"}
            },
            "required": ["answer"]
        }
    
    def teardown_method(self):
        """Clean up test environment."""
        # Remove environment variable
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        client = DeepSeekClient(self.config)
        
        assert client.config == self.config
        assert client.config.api_key == "test-api-key-123"
        assert client.config.base_url == "https://api.deepseek.com"
        assert client.config.model == "deepseek-chat"
    
    def test_client_initialization_missing_api_key(self):
        """Test that client raises error when API key is missing."""
        # Remove API key from environment
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
        
        config = DeepSeekClientConfig(api_key="")
        
        with pytest.raises(ValueError, match="DEEPSEEK_API_KEY environment variable is not set"):
            DeepSeekClient(config)
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_success_text_response(self, mock_openai_class):
        """Test successful LLM call with text response."""
        # Mock the OpenAI client and its response
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        mock_message.content = "I'm doing well, thank you for asking!"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client
        
        # Create client and call LLM
        client = DeepSeekClient(self.config)
        client.client = mock_client  # Replace with mock
        
        response = client.call_llm(self.test_messages)
        
        # Verify the response
        assert response == "I'm doing well, thank you for asking!"
        
        # Verify the API was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        
        assert call_args.kwargs["model"] == self.config.model
        assert call_args.kwargs["messages"] == self.test_messages
        assert call_args.kwargs["temperature"] == self.config.temperature
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_success_json_response(self, mock_openai_class):
        """Test successful LLM call with JSON response."""
        # Mock the OpenAI client and its response
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        json_response = {"answer": "I'm doing well!", "confidence": 0.95}
        mock_message.content = json.dumps(json_response)
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client
        
        # Create client and call LLM
        client = DeepSeekClient(self.config)
        client.client = mock_client  # Replace with mock
        
        response = client.call_llm(self.test_messages, json_schema=self.test_json_schema)
        
        # Verify the response
        assert response == json_response
        
        # Verify the API was called with JSON response format
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        
        assert call_args.kwargs["response_format"] == {"type": "json_object"}
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_invalid_json_response(self, mock_openai_class):
        """Test LLM call with invalid JSON response when JSON schema is provided."""
        # Mock the OpenAI client and its response with invalid JSON
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        mock_message.content = "This is not valid JSON"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client
        
        # Create client and call LLM
        client = DeepSeekClient(self.config)
        client.client = mock_client  # Replace with mock
        
        # Should raise ValueError for invalid JSON
        with pytest.raises(ValueError, match="Failed to parse JSON response"):
            client.call_llm(self.test_messages, json_schema=self.test_json_schema)
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_retry_on_500_error(self, mock_openai_class):
        """Test that client retries on 500 server errors."""
        # Mock the OpenAI client to raise 500 error twice then succeed
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        # Create API errors with status_code 500
        api_error1 = MockAPIError(status_code=500, message="Internal Server Error 1")
        api_error2 = MockAPIError(status_code=500, message="Internal Server Error 2")
        
        # First two calls fail, third succeeds
        mock_client.chat.completions.create.side_effect = [
            api_error1,
            api_error2,
            mock_completion
        ]
        
        mock_message.content = "Success after retries!"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        
        mock_openai_class.return_value = mock_client
        
        # Create client with 2 retries
        config = DeepSeekClientConfig(
            api_key="test-api-key-123",
            max_retries=2,
            retry_delay=0.01  # Short delay for tests
        )
        client = DeepSeekClient(config)
        client.client = mock_client  # Replace with mock
        
        response = client.call_llm(self.test_messages)
        
        # Verify the response
        assert response == "Success after retries!"
        
        # Verify the API was called 3 times (initial + 2 retries)
        assert mock_client.chat.completions.create.call_count == 3
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_retry_on_connection_error(self, mock_openai_class):
        """Test that client retries on connection errors."""
        # Mock the OpenAI client to raise connection error twice then succeed
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        # Create connection errors
        connection_error1 = MockAPIConnectionError(message="Connection failed 1")
        connection_error2 = MockAPIConnectionError(message="Connection failed 2")
        
        # First two calls fail, third succeeds
        mock_client.chat.completions.create.side_effect = [
            connection_error1,
            connection_error2,
            mock_completion
        ]
        
        mock_message.content = "Success after connection retries!"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        
        mock_openai_class.return_value = mock_client
        
        # Create client with 2 retries
        config = DeepSeekClientConfig(
            api_key="test-api-key-123",
            max_retries=2,
            retry_delay=0.01  # Short delay for tests
        )
        client = DeepSeekClient(config)
        client.client = mock_client  # Replace with mock
        
        response = client.call_llm(self.test_messages)
        
        # Verify the response
        assert response == "Success after connection retries!"
        
        # Verify the API was called 3 times (initial + 2 retries)
        assert mock_client.chat.completions.create.call_count == 3
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_no_retry_on_400_error(self, mock_openai_class):
        """Test that client does not retry on 400 client errors."""
        # Mock the OpenAI client to raise 400 error
        mock_client = Mock()
        
        # Create a mock APIError with status_code 400
        api_error = MockAPIError(status_code=400, message="Bad Request")
        
        mock_client.chat.completions.create.side_effect = api_error
        mock_openai_class.return_value = mock_client
        
        # Create client
        client = DeepSeekClient(self.config)
        client.client = mock_client  # Replace with mock
        
        # Should raise the error without retrying
        with pytest.raises(MockAPIError):
            client.call_llm(self.test_messages)
        
        # Verify the API was called only once (no retry for 400 errors)
        assert mock_client.chat.completions.create.call_count == 1
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_exceeds_max_retries(self, mock_openai_class):
        """Test that client raises error after exceeding max retries."""
        # Mock the OpenAI client to always raise 500 error
        mock_client = Mock()
        
        # Create API errors with status_code 500
        api_error1 = MockAPIError(status_code=500, message="Internal Server Error 1")
        api_error2 = MockAPIError(status_code=500, message="Internal Server Error 2")
        
        mock_client.chat.completions.create.side_effect = [api_error1, api_error2]
        mock_openai_class.return_value = mock_client
        
        # Create client with 1 retry
        config = DeepSeekClientConfig(
            api_key="test-api-key-123",
            max_retries=1,
            retry_delay=0.01
        )
        client = DeepSeekClient(config)
        client.client = mock_client  # Replace with mock
        
        # Should raise error after retries
        with pytest.raises(MockAPIError):
            client.call_llm(self.test_messages)
        
        # Verify the API was called 2 times (initial + 1 retry)
        assert mock_client.chat.completions.create.call_count == 2
    
    @patch('app.services.ai.client.OpenAI')
    def test_call_llm_with_custom_parameters(self, mock_openai_class):
        """Test LLM call with custom parameters."""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        mock_message.content = "Custom response"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client
        
        # Create client and call LLM with custom parameters
        client = DeepSeekClient(self.config)
        client.client = mock_client  # Replace with mock
        
        custom_params = {
            "temperature": 0.9,
            "max_tokens": 100,
            "top_p": 0.9
        }
        
        response = client.call_llm(self.test_messages, **custom_params)
        
        # Verify the response
        assert response == "Custom response"
        
        # Verify the API was called with custom parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        
        assert call_args.kwargs["temperature"] == 0.9
        assert call_args.kwargs["max_tokens"] == 100
        assert call_args.kwargs["top_p"] == 0.9
    
    def test_get_deepseek_client_convenience_function(self):
        """Test the convenience function to get a client instance."""
        from app.services.ai.client import get_deepseek_client
        
        # Test with default config
        client1 = get_deepseek_client()
        assert isinstance(client1, DeepSeekClient)
        
        # Test with custom config
        custom_config = DeepSeekClientConfig(
            api_key="custom-key",
            model="deepseek-coder"
        )
        client2 = get_deepseek_client(custom_config)
        assert client2.config == custom_config