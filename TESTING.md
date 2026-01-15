# Integration Testing for Service Alpha

## Overview
This directory contains integration tests for Service Alpha, which validates that the service correctly processes orders by communicating with Service Beta and returns the appropriate order status.

## Test Files

1. **`simple_integration_test.py`** - Basic test that verifies the main requirement
2. **`test_integration.py`** - Comprehensive test suite with multiple test cases

## Requirements
- Python 3.x
- Flask
- requests

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### Simple Test
```bash
python simple_integration_test.py
```

### Comprehensive Test Suite
```bash
python test_integration.py
```

## What the Tests Verify

### Main Requirement (TASK 3)
The tests verify that Service Alpha:
- Processes orders correctly
- Returns `{"order_status": "confirmed"}` for in-stock items

### Additional Validations
1. **Order Confirmation**: Tests that items with stock > 0 return `"order_status": "confirmed"`
2. **Out of Stock Handling**: Tests that items with stock = 0 return `"order_status": "out_of_stock"`
3. **Error Handling**: Validates that connection errors to Service Beta are handled gracefully

## Test Architecture

The tests use a mock Service Beta server that:
- Runs on port 5002
- Returns mock inventory data
- Simulates different scenarios (in-stock, out-of-stock)

Service Alpha runs on port 5001 and communicates with the mock Service Beta.

## Test Results

When tests pass, you should see:
```
✓ SUCCESS: Order status is 'confirmed'!
INTEGRATION TEST PASSED!
Service Alpha correctly processes orders and returns
'order_status: confirmed' as required.
```

## Implementation Details

The integration tests:
1. Start a mock Service Beta server in a separate thread
2. Start Service Alpha in a separate thread
3. Wait for both services to become available
4. Make HTTP requests to Service Alpha's `/order/<item_id>` endpoint
5. Validate the responses match expected behavior

This approach ensures that the entire order processing flow is tested end-to-end, including the inter-service communication between Service Alpha and Service Beta.