#!/usr/bin/env python3
"""
Consolidated test runner for Service Alpha.
Runs all integration tests efficiently in a single command.
"""

import subprocess
import sys
import os

def run_test(test_file, description):
    """Run a single test file and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Test file: {test_file}")
    print('='*60)
    
    try:
        # Run the test with a timeout
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} PASSED")
            return True
        else:
            print(f"✗ {description} FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} TIMED OUT after 30 seconds")
        return False
    except Exception as e:
        print(f"✗ {description} ERROR: {e}")
        return False

def main():
    """Main test runner function."""
    print("="*60)
    print("CONSOLIDATED TEST RUNNER FOR SERVICE ALPHA")
    print("="*60)
    
    # Define tests to run
    tests = [
        ("simple_integration_test.py", "Simple Integration Test"),
        ("test_integration.py", "Comprehensive Integration Test")
    ]
    
    all_passed = True
    passed_count = 0
    total_count = len(tests)
    
    for test_file, description in tests:
        if not os.path.exists(test_file):
            print(f"\n⚠  Test file not found: {test_file}")
            continue
            
        if run_test(test_file, description):
            passed_count += 1
        else:
            all_passed = False
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {total_count}")
    print(f"Tests passed: {passed_count}")
    print(f"Tests failed: {total_count - passed_count}")
    
    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print("\n✗ SOME TESTS FAILED")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest runner interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error in test runner: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)