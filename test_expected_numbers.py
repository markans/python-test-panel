#!/usr/bin/env python3
"""
Test the expected phone numbers with their expected results
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_expected_numbers():
    """Test the specific numbers with expected results"""
    print("=" * 70)
    print("TESTING EXPECTED PHONE NUMBERS")
    print("=" * 70)
    
    # Your expected numbers and their results
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
    
    print("\nExpected Results:")
    for num, status in expected_results.items():
        icon = "✅" if status == "connected" else "❌"
        print(f"  {icon} {num} - {status}")
    
    print("\n" + "-" * 70)
    
    # Start test with shorter timeouts for faster testing
    max_wait = 15  # 15 seconds max wait
    idle = 5       # 5 seconds idle after connected
    
    print(f"\nTest Settings:")
    print(f"  Max wait time: {max_wait} seconds")
    print(f"  Idle time: {idle} seconds")
    print(f"  Total numbers: {len(test_numbers)}")
    
    # Start the test
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test_numbers,
        "max_wait_seconds": max_wait,
        "idle_seconds": idle
    })
    
    if response.status_code != 200:
        print(f"Failed to start test: {response.text}")
        return
    
    print("\n✓ Test started successfully")
    print("\n" + "=" * 70)
    print("REAL-TIME PROGRESS:")
    print("=" * 70)
    
    # Monitor progress
    start_time = time.time()
    last_tested = 0
    
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        
        # Print when a number is completed
        if status['tested_numbers'] > last_tested:
            print(f"\n[{time.time() - start_time:5.1f}s] Completed {status['tested_numbers']}/{status['total_numbers']}")
            print(f"  Connected so far: {status['connected_numbers']}")
            print(f"  Failed so far: {status['failed_numbers']}")
            last_tested = status['tested_numbers']
        
        # Show current number being tested
        if status['current_number']:
            print(f"\r  Testing: {status['current_number']}...", end='', flush=True)
        
        if not status['is_running'] and status['tested_numbers'] > 0:
            print()  # New line
            break
        
        time.sleep(0.5)
    
    # Get final results
    print("\n" + "=" * 70)
    print("FINAL RESULTS:")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    # Check results against expectations
    all_correct = True
    for result in results:
        number = result['phone_number']
        actual_status = "connected" if result['status'] == 'connected' else "failed"
        expected_status = expected_results.get(number, "unknown")
        
        if actual_status == expected_status:
            icon = "✅"
            match = "CORRECT"
        else:
            icon = "❌"
            match = "WRONG"
            all_correct = False
        
        print(f"\n{icon} {number}:")
        print(f"   Expected: {expected_status}")
        print(f"   Actual: {result['status']}")
        print(f"   Result: {match}")
        if result.get('sip_code'):
            print(f"   SIP Code: {result['sip_code']}")
        if result.get('wait_time'):
            print(f"   Response Time: {result['wait_time']:.1f}s")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    total_time = time.time() - start_time
    print(f"Total test time: {total_time:.1f} seconds")
    print(f"Connected: {len(status['connected_numbers'])} numbers")
    print(f"Failed: {len(status['failed_numbers'])} numbers")
    
    if status['connected_numbers']:
        print(f"\n✅ Connected numbers:")
        for num in status['connected_numbers']:
            print(f"   • {num}")
    
    if status['failed_numbers']:
        print(f"\n❌ Failed numbers:")
        for num in status['failed_numbers']:
            print(f"   • {num}")
    
    # Verification
    print("\n" + "=" * 70)
    if all_correct:
        print("✅ SUCCESS: All numbers matched expected results!")
    else:
        print("❌ FAILURE: Some numbers did not match expected results")
    
    # Compare with expected
    print("\n" + "=" * 70)
    print("COMPARISON WITH EXPECTED:")
    print("=" * 70)
    
    expected_connected = ["907086197000", "902161883006", "3698446014"]
    expected_failed = ["639758005031"]
    
    actual_connected = [r['phone_number'] for r in results if r['status'] == 'connected']
    actual_failed = [r['phone_number'] for r in results if r['status'] != 'connected']
    
    print(f"\nExpected Connected: {expected_connected}")
    print(f"Actual Connected:   {actual_connected}")
    print(f"Match: {set(expected_connected) == set(actual_connected)}")
    
    print(f"\nExpected Failed: {expected_failed}")
    print(f"Actual Failed:   {actual_failed}")
    print(f"Match: {set(expected_failed) == set(actual_failed)}")

if __name__ == '__main__':
    # Wait for app to be ready
    time.sleep(2)
    test_expected_numbers()