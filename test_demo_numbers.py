#!/usr/bin/env python3
"""
Test script to verify the expected demo phone numbers work correctly
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

def test_demo_numbers():
    """Test the demo numbers with expected results"""
    
    print_header("🔍 TESTING DEMO PHONE NUMBERS")
    
    # Test numbers with expected results
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
    
    print(f"\n{BOLD}Expected Results:{RESET}")
    for num, status in expected_results.items():
        icon = f"{GREEN}✅{RESET}" if status == "connected" else f"{RED}❌{RESET}"
        print(f"  {icon} {num} - {status}")
    
    print(f"\n{'-'*70}")
    
    # Configure test settings for faster demo
    max_wait = 15  # 15 seconds max wait
    idle = 5       # 5 seconds idle after connected calls
    
    print(f"\n{BOLD}Test Settings:{RESET}")
    print(f"  • Max wait time: {max_wait} seconds")
    print(f"  • Idle time: {idle} seconds")
    print(f"  • Total numbers: {len(test_numbers)}")
    
    # Start the test
    print(f"\n{BLUE}Starting test...{RESET}")
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test_numbers,
        "max_wait_seconds": max_wait,
        "idle_seconds": idle
    })
    
    if response.status_code != 200:
        print(f"{RED}Failed to start test: {response.text}{RESET}")
        return
    
    print(f"{GREEN}✓ Test started successfully{RESET}")
    
    print_header("📊 REAL-TIME PROGRESS")
    
    # Monitor progress
    start_time = time.time()
    last_tested = 0
    
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        
        # Print progress updates
        if status['tested_numbers'] > last_tested:
            elapsed = time.time() - start_time
            print(f"\n[{elapsed:5.1f}s] Completed {status['tested_numbers']}/{status['total_numbers']}")
            
            if status['connected_numbers']:
                print(f"  {GREEN}Connected: {status['connected_numbers']}{RESET}")
            if status['failed_numbers']:
                print(f"  {RED}Failed: {status['failed_numbers']}{RESET}")
            
            last_tested = status['tested_numbers']
        
        # Show current number being tested
        if status['current_number']:
            print(f"\r  {BLUE}Testing: {status['current_number']}...{RESET}", end='', flush=True)
        
        if not status['is_running'] and status['tested_numbers'] > 0:
            print()  # New line
            break
        
        time.sleep(0.5)
    
    # Get final results
    print_header("✅ FINAL RESULTS")
    
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    # Analyze results
    all_correct = True
    for result in results:
        number = result['phone_number']
        actual_status = "connected" if result['status'] == 'connected' else "failed"
        expected_status = expected_results.get(number, "unknown")
        
        if actual_status == expected_status:
            icon = f"{GREEN}✅{RESET}"
            match = f"{GREEN}CORRECT{RESET}"
        else:
            icon = f"{RED}❌{RESET}"
            match = f"{RED}WRONG{RESET}"
            all_correct = False
        
        print(f"\n{icon} {BOLD}{number}:{RESET}")
        print(f"   Expected: {expected_status}")
        print(f"   Actual: {result['status']}")
        print(f"   Result: {match}")
        
        if result.get('sip_code'):
            print(f"   SIP Code: {result['sip_code']}")
        if result.get('wait_time'):
            print(f"   Response Time: {result['wait_time']:.1f}s")
    
    # Summary
    print_header("📈 SUMMARY")
    
    total_time = time.time() - start_time
    print(f"Total test time: {total_time:.1f} seconds")
    print(f"Connected: {len(status['connected_numbers'])} numbers")
    print(f"Failed: {len(status['failed_numbers'])} numbers")
    
    if status['connected_numbers']:
        print(f"\n{GREEN}✅ Connected numbers:{RESET}")
        for num in status['connected_numbers']:
            print(f"   • {num}")
    
    if status['failed_numbers']:
        print(f"\n{RED}❌ Failed numbers:{RESET}")
        for num in status['failed_numbers']:
            print(f"   • {num}")
    
    # Final verification
    print_header("🎯 VERIFICATION")
    
    if all_correct:
        print(f"{GREEN}{BOLD}SUCCESS: All numbers matched expected results!{RESET}")
        print(f"\n{GREEN}The system is working correctly with the expected demo numbers.{RESET}")
    else:
        print(f"{RED}{BOLD}FAILURE: Some numbers did not match expected results{RESET}")
        print(f"\n{YELLOW}Please check the configuration and try again.{RESET}")
    
    # Show expected vs actual comparison
    print(f"\n{BOLD}Comparison:{RESET}")
    
    expected_connected = ["907086197000", "902161883006", "3698446014"]
    expected_failed = ["639758005031"]
    
    actual_connected = [r['phone_number'] for r in results if r['status'] == 'connected']
    actual_failed = [r['phone_number'] for r in results if r['status'] != 'connected']
    
    print(f"\nExpected Connected: {expected_connected}")
    print(f"Actual Connected:   {actual_connected}")
    connected_match = set(expected_connected) == set(actual_connected)
    print(f"Match: {GREEN if connected_match else RED}{connected_match}{RESET}")
    
    print(f"\nExpected Failed: {expected_failed}")
    print(f"Actual Failed:   {actual_failed}")
    failed_match = set(expected_failed) == set(actual_failed)
    print(f"Match: {GREEN if failed_match else RED}{failed_match}{RESET}")
    
    return all_correct

if __name__ == '__main__':
    # Wait a moment for the server to be ready
    time.sleep(1)
    
    print(f"{BOLD}Phone Number Test Panel - Demo Verification{RESET}")
    print("This script tests the expected demo numbers to ensure they work correctly.")
    
    success = test_demo_numbers()
    
    print(f"\n{'='*70}")
    if success:
        print(f"{GREEN}{BOLD}✅ All tests passed successfully!{RESET}")
    else:
        print(f"{YELLOW}{BOLD}⚠️ Some tests did not pass as expected.{RESET}")
    print(f"{'='*70}\n")