"""
LLM Engine for DeepSeek API integration.
Handles specification extraction and comparison using DeepSeek LLM.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from openai import OpenAI

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class LLMEngine:
    """Engine for interacting with DeepSeek LLM API."""
    
    def __init__(self):
        """Initialize DeepSeek client with configuration from settings."""
        # Initialize client only if API key is available
        self.client = None
        if settings.DEEPSEEK_API_KEY:
            self.client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )
            logger.info(f"LLMEngine initialized with model: {settings.DEEPSEEK_MODEL}, base_url: {settings.DEEPSEEK_BASE_URL}")
        else:
            logger.warning("LLMEngine initialized without API key. API calls will fail.")
        
        self.model = settings.DEEPSEEK_MODEL
        self.temperature = settings.DEEPSEEK_TEMPERATURE
        self.max_tokens = settings.DEEPSEEK_MAX_TOKENS
        
        # Setup log directory
        self.log_dir = "logs/llm"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def _log_interaction(self, prompt: str, response: str, function_name: str):
        """Log prompt and response to a file for debugging."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"{function_name}_{timestamp}.log")
        
        log_content = f"""=== {function_name} - {timestamp} ===
PROMPT:
{prompt}

RESPONSE:
{response}
{"="*50}
"""
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.log_dir, exist_ok=True)
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            logger.debug(f"Logged interaction to {log_file}")
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
    
    def _call_llm(self, prompt: str, system_message: str = None, json_mode: bool = True) -> str:
        """
        Call DeepSeek LLM with given prompt.
        
        Args:
            prompt: User prompt
            system_message: System message (optional)
            json_mode: Whether to request JSON response format
            
        Returns:
            Raw response text from LLM
            
        Raises:
            RuntimeError: If client is not initialized (no API key)
        """
        if not self.client:
            raise RuntimeError("LLM client not initialized. DEEPSEEK_API_KEY is required.")
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response_format = {"type": "json_object"} if json_mode else None
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format
            )
            
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            raise
    
    def extract_specs(self, text: str, ktru: str = None) -> Dict[str, Any]:
        """
        Extract specifications from text using LLM.
        
        Args:
            text: Text containing product specifications
            ktru: KTRU code (optional)
            
        Returns:
            Dictionary with extracted specifications
        """
        # System message for specification extraction
        system_message = """You are a technical specification extraction assistant. 
        Extract product specifications from the provided text and return them in a structured JSON format.
        Be precise and extract all relevant technical parameters."""
        
        # Prompt for specification extraction
        prompt = f"""Extract product specifications from the following text:

TEXT:
{text}

{"KTRU CODE: " + ktru if ktru else ""}

Return a JSON object with the following structure:
{{
  "product_name": "extracted product name",
  "manufacturer": "extracted manufacturer name",
  "model": "extracted model number",
  "technical_specs": {{
    "key1": "value1",
    "key2": "value2",
    ...
  }},
  "quantity": extracted_quantity_if_available,
  "unit_price": extracted_unit_price_if_available,
  "total_price": extracted_total_price_if_available,
  "delivery_terms": "extracted delivery terms if available",
  "warranty": "extracted warranty information if available"
}}

If any field cannot be extracted from the text, use null for that field.
Ensure the response is valid JSON only, with no additional text."""
        
        try:
            # Call LLM
            raw_response = self._call_llm(prompt, system_message, json_mode=True)
            
            # Log interaction
            self._log_interaction(prompt, raw_response, "extract_specs")
            
            # Parse JSON response
            result = json.loads(raw_response)
            
            # Add metadata
            result["extraction_timestamp"] = datetime.now().isoformat()
            if ktru:
                result["ktru_code"] = ktru
            
            logger.info(f"Successfully extracted specifications from text (length: {len(text)} chars)")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}\nResponse: {raw_response}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Error in extract_specs: {e}")
            raise
    
    def compare_specs(self, target_json: Dict[str, Any], contract_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare target specifications with contract specifications.
        
        Args:
            target_json: Target product specifications
            contract_json: Contract product specifications
            
        Returns:
            Dictionary with comparison results
        """
        # System message for comparison
        system_message = """You are a technical specification comparison assistant. 
        Compare two sets of product specifications and identify matches, mismatches, and compatibility.
        Be objective and focus on technical parameters."""
        
        # Prepare comparison prompt
        prompt = f"""Compare the following two sets of product specifications:

TARGET SPECIFICATIONS:
{json.dumps(target_json, indent=2, ensure_ascii=False)}

CONTRACT SPECIFICATIONS:
{json.dumps(contract_json, indent=2, ensure_ascii=False)}

Return a JSON object with the following comparison structure:
{{
  "overall_match_score": 0.95,  # Overall match score from 0.0 to 1.0
  "manufacturer_match": true/false,  # Whether manufacturers match
  "model_match": true/false,  # Whether models match
  "technical_comparison": {{
    "parameter1": {{
      "target_value": "value1",
      "contract_value": "value1",
      "match": true,
      "notes": "optional notes"
    }},
    "parameter2": {{
      "target_value": "value2",
      "contract_value": "different_value2",
      "match": false,
      "notes": "values differ"
    }}
  }},
  "critical_mismatches": ["list of critical parameter mismatches if any"],
  "recommendation": "recommendation text (e.g., 'Good match', 'Partial match with minor differences', 'Significant mismatches')",
  "compatibility_assessment": "assessment of overall compatibility"
}}

Ensure the response is valid JSON only, with no additional text."""
        
        try:
            # Call LLM
            raw_response = self._call_llm(prompt, system_message, json_mode=True)
            
            # Log interaction
            self._log_interaction(prompt, raw_response, "compare_specs")
            
            # Parse JSON response
            result = json.loads(raw_response)
            
            # Add metadata
            result["comparison_timestamp"] = datetime.now().isoformat()
            result["target_product"] = target_json.get("product_name", "Unknown")
            result["contract_product"] = contract_json.get("product_name", "Unknown")
            
            logger.info(f"Successfully compared specifications for {result['target_product']} vs {result['contract_product']}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}\nResponse: {raw_response}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Error in compare_specs: {e}")
            raise
    
    def batch_extract_specs(self, texts: List[str], ktru_codes: List[str] = None) -> List[Dict[str, Any]]:
        """
        Extract specifications from multiple texts.
        
        Args:
            texts: List of texts containing product specifications
            ktru_codes: List of KTRU codes (optional, must match texts length if provided)
            
        Returns:
            List of extracted specifications
        """
        if ktru_codes and len(texts) != len(ktru_codes):
            raise ValueError("Number of texts must match number of KTRU codes")
        
        results = []
        for i, text in enumerate(texts):
            ktru = ktru_codes[i] if ktru_codes else None
            try:
                specs = self.extract_specs(text, ktru)
                results.append(specs)
            except Exception as e:
                logger.error(f"Failed to extract specs for item {i}: {e}")
                results.append({"error": str(e), "text_index": i})
        
        return results


# Create singleton instance
llm_engine = LLMEngine()