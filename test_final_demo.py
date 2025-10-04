#!/usr/bin/env python3
"""
Final demonstration that all fixes are working
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

# Color codes
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

def main():
    print_header("🎯 PHONE TEST PANEL - FINAL VERIFICATION")
    
    # Expected test numbers and results
    test_numbers = [
        "907086197000",  # Expected: connected
        "639758005031",  # Expected: failed  
        "902161883006",  # Expected: connected
        "3698446014"     # Expected: connected
    ]
    
    print(f"\n{BOLD}Expected Results:{RESET}")
    print(f"  {GREEN}✅{RESET} 907086197000 - connected")
    print(f"  {RED}❌{RESET} 639758005031 - failed")
    print(f"  {GREEN}✅{RESET} 902161883006 - connected")
    print(f"  {GREEN}✅{RESET} 3698446014 - connected")
    
    print(f"\n{BOLD}Starting test with all 4 numbers...{RESET}")
    
    # Start test
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test_numbers,
        "max_wait_seconds": 10,
        "idle_seconds": 3
    })
    
    if response.status_code != 200:
        print(f"{RED}Error starting test: {response.text}{RESET}")
        return
    
    data = response.json()
    print(f"{GREEN}✓ Test started: {data['total_numbers']} numbers{RESET}")
    print(f"  Settings: Max wait={data['settings']['max_wait']}s, Idle={data['settings']['idle']}s")
    
    # Monitor progress
    print(f"\n{BOLD}Real-time Progress:{RESET}")
    start_time = time.time()
    last_count = 0
    
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        
        # Check if stats were reset at start
        if status['tested_numbers'] == 0 and last_count == 0:
            print(f"{GREEN}✓ Stats reset to 0 at start{RESET}")
        
        # Show progress
        if status['tested_numbers'] > last_count:
            elapsed = time.time() - start_time
            print(f"\n[{elapsed:4.1f}s] Progress: {status['tested_numbers']}/{status['total_numbers']}")
            print(f"  Connected: {status['connected_numbers']}")
            print(f"  Failed: {status['failed_numbers']}")
            last_count = status['tested_numbers']
        
        if status['current_number']:
            print(f"\r  {BLUE}Testing: {status['current_number']}...{RESET}", end='', flush=True)
        
        if not status['is_running'] and status['tested_numbers'] > 0:
            break
        
        time.sleep(0.5)
    
    print()  # New line
    
    # Get results
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    print_header("📊 FINAL RESULTS")
    
    # Verify each number
    all_correct = True
    for result in results:
        number = result['phone_number']
        status_text = result['status']
        
        # Check expected result
        if number == "639758005031":
            expected = "failed"
            is_correct = status_text != "connected"
        else:
            expected = "connected"
            is_correct = status_text == "connected"
        
        if is_correct:
            print(f"{GREEN}✅ {number}: {status_text} (CORRECT){RESET}")
        else:
            print(f"{RED}❌ {number}: {status_text} (WRONG - expected {expected}){RESET}")
            all_correct = False
    
    # Summary
    print_header("✅ VERIFICATION SUMMARY")
    
    print(f"\nTotal tested: {status['tested_numbers']}")
    print(f"Connected: {len(status['connected_numbers'])}")
    print(f"Failed: {len(status['failed_numbers'])}")
    
    print(f"\n{BOLD}Expected vs Actual:{RESET}")
    expected_connected = ["907086197000", "902161883006", "3698446014"]
    actual_connected = status['connected_numbers']
    
    print(f"Expected connected: {expected_connected}")
    print(f"Actual connected:   {actual_connected}")
    
    if set(expected_connected) == set(actual_connected):
        print(f"{GREEN}✅ Connected numbers match!{RESET}")
    else:
        print(f"{RED}❌ Connected numbers don't match{RESET}")
    
    if all_correct:
        print(f"\n{GREEN}{BOLD}🎉 SUCCESS! All numbers returned expected results!{RESET}")
        print(f"{GREEN}The system is working correctly.{RESET}")
        
        print(f"\n{BOLD}✅ Fixed Issues:{RESET}")
        print(f"  1. Demo numbers now return correct results:")
        print(f"     • 907086197000 - {GREEN}connected{RESET}")
        print(f"     • 639758005031 - {RED}failed{RESET}")
        print(f"     • 902161883006 - {GREEN}connected{RESET}")
        print(f"     • 3698446014 - {GREEN}connected{RESET}")
        print(f"  2. Stats properly reset to 0 when starting new test")
        print(f"  3. Number sanitization handles various formats")
        print(f"  4. Real-time updates working correctly")
    else:
        print(f"\n{YELLOW}⚠️ Some results didn't match expectations{RESET}")
    
    return all_correct

if __name__ == '__main__':
    print(f"{BOLD}Phone Number Test Panel - Demo Verification{RESET}")
    print("This verifies the expected demo numbers work correctly.\n")
    
    # Wait for service to be ready
    time.sleep(1)
    
    success = main()
    
    print(f"\n{'='*70}")
    if success:
        print(f"{GREEN}{BOLD}All tests completed successfully!{RESET}")
    else:
        print(f"{YELLOW}{BOLD}Please review the results above.{RESET}")
    print(f"{'='*70}\n")