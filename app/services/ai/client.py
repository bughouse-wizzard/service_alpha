"""
DeepSeek Client Wrapper for Service Alpha.
Provides a generic interface to call DeepSeek LLM API with timeout handling,
retry logic, and JSON response parsing.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from openai import OpenAI, APIConnectionError, APIError, RateLimitError
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for AI client
ai_logger = logging.getLogger("ai_client")
ai_logger.setLevel(logging.INFO)

# Create file handler for AI-specific logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "ai_client_debug.log")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ai_logger.addHandler(file_handler)


class DeepSeekClientConfig(BaseModel):
    """Configuration for DeepSeek client."""
    api_key: str = Field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", ""))
    base_url: str = Field(default="https://api.deepseek.com")
    model: str = Field(default="deepseek-chat")
    timeout: int = Field(default=30, ge=1, description="Request timeout in seconds")
    max_retries: int = Field(default=3, ge=0, description="Maximum number of retries for failed requests")
    retry_delay: float = Field(default=1.0, ge=0.0, description="Delay between retries in seconds")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)


class DeepSeekClient:
    """Client wrapper for DeepSeek LLM API."""
    
    def __init__(self, config: Optional[DeepSeekClientConfig] = None):
        """Initialize DeepSeek client.
        
        Args:
            config: Configuration for the client. If None, uses default config.
        """
        self.config = config or DeepSeekClientConfig()
        
        if not self.config.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
        
        ai_logger.info(f"DeepSeek client initialized with model: {self.config.model}")
    
    def _log_request(self, messages: List[Dict[str, str]], json_schema: Optional[Dict[str, Any]] = None) -> str:
        """Log the request details and return a request ID."""
        request_id = f"req_{int(time.time() * 1000)}"
        
        log_data = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "model": self.config.model,
            "messages": messages,
            "json_schema": json_schema,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        ai_logger.info(f"Request {request_id}: {json.dumps(log_data, ensure_ascii=False)}")
        return request_id
    
    def _log_response(self, request_id: str, response: Any, raw_response: Optional[str] = None):
        """Log the response details."""
        # Handle non-serializable objects
        try:
            response_str = str(response)
        except Exception:
            response_str = f"<Non-serializable object: {type(response).__name__}>"
        
        log_data = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "response": response_str,
            "raw_response": raw_response
        }
        
        ai_logger.info(f"Response {request_id}: {json.dumps(log_data, ensure_ascii=False)}")
    
    def _log_error(self, request_id: str, error: Exception, attempt: int):
        """Log error details."""
        error_data = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "attempt": attempt
        }
        
        ai_logger.error(f"Error {request_id}: {json.dumps(error_data, ensure_ascii=False)}")
    
    def call_llm(
        self,
        messages: List[Dict[str, str]],
        json_schema: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[Dict[str, Any], str]:
        """Call DeepSeek LLM with the given messages and optional JSON schema.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            json_schema: Optional JSON schema for structured output.
            **kwargs: Additional parameters to pass to the API call.
            
        Returns:
            Parsed JSON response if json_schema is provided, otherwise raw text.
            
        Raises:
            APIConnectionError: If connection to API fails after retries.
            APIError: If API returns an error.
            ValueError: If response cannot be parsed as JSON when json_schema is provided.
        """
        # Log the request
        request_id = self._log_request(messages, json_schema)
        
        # Prepare API parameters
        api_params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            **kwargs
        }
        
        if self.config.max_tokens:
            api_params["max_tokens"] = self.config.max_tokens
        
        # Add JSON schema if provided
        if json_schema:
            api_params["response_format"] = {"type": "json_object"}
        
        # Retry logic
        last_error = None
        for attempt in range(1, self.config.max_retries + 2):  # +1 for initial attempt
            try:
                ai_logger.info(f"Request {request_id}: Attempt {attempt}/{self.config.max_retries + 1}")
                
                # Make API call
                response = self.client.chat.completions.create(**api_params)
                
                # Extract content
                content = response.choices[0].message.content
                
                # Log raw response
                self._log_response(request_id, content, raw_response=str(response))
                
                # Parse JSON if schema was provided
                if json_schema and content:
                    try:
                        parsed = json.loads(content)
                        ai_logger.info(f"Request {request_id}: Successfully parsed JSON response")
                        return parsed
                    except json.JSONDecodeError as e:
                        error_msg = f"Failed to parse JSON response: {e}"
                        ai_logger.error(f"Request {request_id}: {error_msg}")
                        raise ValueError(error_msg) from e
                
                # Return raw content if no JSON schema
                return content
                
            except (APIConnectionError, APIError, RateLimitError) as e:
                last_error = e
                self._log_error(request_id, e, attempt)
                
                # Check if we should retry
                if attempt <= self.config.max_retries:
                    # Check if it's a 5xx error (server error) that we should retry
                    if hasattr(e, 'status_code') and e.status_code and 500 <= e.status_code < 600:
                        ai_logger.warning(f"Request {request_id}: Server error {e.status_code}, retrying in {self.config.retry_delay}s")
                        time.sleep(self.config.retry_delay)
                    elif isinstance(e, (APIConnectionError, RateLimitError)):
                        # Retry on connection errors and rate limits
                        ai_logger.warning(f"Request {request_id}: {type(e).__name__}, retrying in {self.config.retry_delay}s")
                        time.sleep(self.config.retry_delay)
                    else:
                        # Don't retry on other errors
                        break
                else:
                    break
        
        # If we get here, all retries failed
        error_msg = f"Failed after {self.config.max_retries + 1} attempts"
        ai_logger.error(f"Request {request_id}: {error_msg}")
        
        if last_error:
            raise last_error
        else:
            raise APIError(f"Unknown error: {error_msg}")


# Convenience function for quick usage
def get_deepseek_client(config: Optional[DeepSeekClientConfig] = None) -> DeepSeekClient:
    """Get a DeepSeek client instance.
    
    Args:
        config: Optional configuration. If None, uses default config.
        
    Returns:
        DeepSeekClient instance.
    """
    return DeepSeekClient(config)