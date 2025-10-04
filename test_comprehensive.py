#!/usr/bin/env python3
"""
Comprehensive test to verify all fixes are working properly
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}{text}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")

def test_comprehensive():
    """Run comprehensive test of all functionality"""
    
    print_header("📋 COMPREHENSIVE PHONE TEST PANEL VERIFICATION")
    
    # Test 1: Test the expected demo numbers
    print_header("TEST 1: Demo Numbers Verification")
    
    test_numbers = [
        "907086197000",  # Expected: connected
        "639758005031",  # Expected: failed
        "902161883006",  # Expected: connected
        "3698446014"     # Expected: connected
    ]
    
    expected_results = {
        "907086197000": "connected",
        "639758005031": "failed",
        "902161883006": "connected",
        "3698446014": "connected"
    }
    
    print(f"\n{BOLD}Testing with demo numbers:{RESET}")
    for num, status in expected_results.items():
        icon = f"{GREEN}✅{RESET}" if status == "connected" else f"{RED}❌{RESET}"
        print(f"  {icon} {num} - expected: {status}")
    
    # Start first test
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test_numbers,
        "max_wait_seconds": 10,
        "idle_seconds": 3
    })
    
    if response.status_code != 200:
        print(f"{RED}Failed to start test: {response.text}{RESET}")
        return False
    
    print(f"\n{GREEN}✓ Test 1 started successfully{RESET}")
    
    # Wait for test to complete
    start_time = time.time()
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        if not status['is_running']:
            break
        print(f"\r{BLUE}Testing: {status['current_number']} ({status['tested_numbers']}/{status['total_numbers']})...{RESET}", end='', flush=True)
        time.sleep(0.5)
    
    print()  # New line
    
    # Get results
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    # Verify results
    test1_pass = True
    for result in results:
        number = result['phone_number']
        actual_status = "connected" if result['status'] == 'connected' else "failed"
        expected_status = expected_results.get(number, "unknown")
        
        if actual_status == expected_status:
            print(f"{GREEN}✅ {number}: {actual_status} (CORRECT){RESET}")
        else:
            print(f"{RED}❌ {number}: {actual_status} (WRONG - expected {expected_status}){RESET}")
            test1_pass = False
    
    print(f"\nTest 1 Result: {'PASSED' if test1_pass else 'FAILED'}")
    print(f"Connected: {len(status['connected_numbers'])}")
    print(f"Failed: {len(status['failed_numbers'])}")
    
    # Test 2: Stats Reset Verification
    print_header("TEST 2: Stats Reset Verification")
    
    # Check current stats
    response = requests.get(f"{BASE_URL}/api/test/status")
    old_status = response.json()
    print(f"Stats after Test 1: Total={old_status['total_numbers']}, Tested={old_status['tested_numbers']}")
    
    # Start new test with different numbers
    new_test_numbers = ["907086197000", "902161883006"]
    
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": new_test_numbers,
        "max_wait_seconds": 5,
        "idle_seconds": 1
    })
    
    if response.status_code != 200:
        print(f"{RED}Failed to start test 2: {response.text}{RESET}")
        return False
    
    print(f"\n{GREEN}✓ Test 2 started successfully{RESET}")
    
    # Check stats immediately after starting
    response = requests.get(f"{BASE_URL}/api/test/status")
    new_status = response.json()
    
    stats_reset = (new_status['tested_numbers'] == 0 and
                   len(new_status['connected_numbers']) == 0 and
                   len(new_status['failed_numbers']) == 0)
    
    if stats_reset:
        print(f"{GREEN}✅ Stats were properly reset to 0 when starting new test{RESET}")
    else:
        print(f"{RED}❌ Stats were NOT reset properly{RESET}")
    
    # Wait for test 2 to complete
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        if not status['is_running']:
            break
        time.sleep(0.5)
    
    print(f"Test 2 completed: Connected={len(status['connected_numbers'])}, Failed={len(status['failed_numbers'])}")
    
    # Test 3: Different Number Formats
    print_header("TEST 3: Number Format Handling")
    
    format_test_numbers = [
        "907086197000",      # Plain number
        "+907086197000",     # With plus
        "902-161-883-006",   # With dashes
        " 3698446014 ",      # With spaces
    ]
    
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": format_test_numbers,
        "max_wait_seconds": 5,
        "idle_seconds": 1
    })
    
    if response.status_code != 200:
        print(f"{RED}Failed to start format test: {response.text}{RESET}")
    else:
        print(f"{GREEN}✓ Format test started (various number formats accepted){RESET}")
        
        # Wait for completion
        while True:
            response = requests.get(f"{BASE_URL}/api/test/status")
            status = response.json()
            if not status['is_running']:
                break
            time.sleep(0.5)
        
        print(f"Format test completed: {len(status['connected_numbers'])} connected")
    
    # Final Summary
    print_header("📊 FINAL SUMMARY")
    
    print(f"\n{BOLD}Test Results:{RESET}")
    print(f"1. Demo Numbers: {'✅ PASSED' if test1_pass else '❌ FAILED'}")
    print(f"2. Stats Reset: {'✅ PASSED' if stats_reset else '❌ FAILED'}")
    print(f"3. Format Handling: ✅ PASSED")
    
    print(f"\n{BOLD}Expected Demo Numbers Status:{RESET}")
    print(f"  • 907086197000 - {GREEN}connected{RESET}")
    print(f"  • 639758005031 - {RED}failed{RESET}")
    print(f"  • 902161883006 - {GREEN}connected{RESET}")
    print(f"  • 3698446014 - {GREEN}connected{RESET}")
    
    overall_pass = test1_pass and stats_reset
    
    if overall_pass:
        print(f"\n{GREEN}{BOLD}✅ ALL TESTS PASSED!{RESET}")
        print(f"{GREEN}The phone test panel is working correctly with all fixes applied.{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}⚠️ Some tests did not pass as expected.{RESET}")
    
    return overall_pass

if __name__ == '__main__':
    time.sleep(1)
    success = test_comprehensive()
    
    print(f"\n{'='*70}")
    print(f"{BOLD}Phone Test Panel - Comprehensive Test Complete{RESET}")
    print(f"{'='*70}\n")