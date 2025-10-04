#!/usr/bin/env python3
"""
Test real-time connection detection with custom timing
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_with_timing():
    """Test with custom timing settings"""
    print("=" * 60)
    print("REAL-TIME CONNECTION TEST")
    print("=" * 60)
    
    # Test configuration
    test_numbers = [
        "63322683000",  # Known test number - should connect quickly
        "999999999",    # Invalid number - should fail
        "1234567890"    # Another test number
    ]
    
    max_wait = 15  # 15 seconds max wait for answer
    idle = 5       # 5 seconds idle after connected calls
    
    print(f"\nTest Configuration:")
    print(f"  Numbers to test: {', '.join(test_numbers)}")
    print(f"  Max wait time: {max_wait} seconds")
    print(f"  Idle time: {idle} seconds")
    print("-" * 60)
    
    # Start test
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test_numbers,
        "max_wait_seconds": max_wait,
        "idle_seconds": idle
    })
    
    if response.status_code != 200:
        print(f"Failed to start test: {response.text}")
        return
    
    data = response.json()
    print(f"\n✓ Test started successfully")
    print(f"  Total numbers: {data['total_numbers']}")
    print(f"  Settings: Wait={data['settings']['max_wait']}s, Idle={data['settings']['idle']}s")
    
    # Monitor progress
    print("\n" + "=" * 60)
    print("MONITORING PROGRESS:")
    print("=" * 60)
    
    start_time = time.time()
    last_number = None
    number_times = {}
    
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        
        # Track timing for each number
        current = status['current_number']
        if current and current != last_number:
            number_times[current] = time.time()
            last_number = current
        
        # Print progress every second
        if status['is_running']:
            elapsed = time.time() - start_time
            print(f"\r[{elapsed:5.1f}s] Testing: {current or 'preparing':<15} | "
                  f"Progress: {status['tested_numbers']}/{status['total_numbers']} | "
                  f"Connected: {len(status['connected_numbers'])} | "
                  f"Failed: {len(status['failed_numbers'])}", end='', flush=True)
        
        if not status['is_running'] and status['tested_numbers'] > 0:
            print()  # New line
            break
        
        time.sleep(0.5)
    
    # Get results
    print("\n" + "=" * 60)
    print("TEST RESULTS:")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    total_time = time.time() - start_time
    
    for result in results:
        icon = "✅" if result['status'] == 'connected' else "❌"
        wait_time = result.get('wait_time', result.get('duration', 0))
        
        print(f"\n{icon} {result['phone_number']}:")
        print(f"   Status: {result['status'].upper()}")
        print(f"   Response time: {wait_time:.1f}s")
        
        if result['status'] == 'connected':
            print(f"   Action: Connected immediately, then idle for {idle}s")
        else:
            print(f"   Reason: {result.get('error', 'No answer within timeout')}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    print(f"Total test time: {total_time:.1f} seconds")
    print(f"Connected numbers: {len(status['connected_numbers'])}")
    print(f"Failed numbers: {len(status['failed_numbers'])}")
    
    if status['connected_numbers']:
        print(f"\n✅ Connected: {', '.join(status['connected_numbers'])}")
    if status['failed_numbers']:
        print(f"❌ Failed: {', '.join(status['failed_numbers'])}")
    
    # Verify behavior
    print("\n" + "=" * 60)
    print("BEHAVIOR VERIFICATION:")
    print("=" * 60)
    
    # Check if 63322683000 connected quickly
    test_num_result = next((r for r in results if '63322683000' in r['phone_number']), None)
    if test_num_result:
        if test_num_result['status'] == 'connected':
            wait = test_num_result.get('wait_time', 0)
            if wait < 5:  # Should connect within 5 seconds
                print(f"✅ PASS: 63322683000 connected quickly ({wait:.1f}s)")
            else:
                print(f"⚠️  WARNING: 63322683000 took {wait:.1f}s to connect")
        else:
            print(f"❌ FAIL: 63322683000 did not connect")
    
    # Verify timing
    expected_time = 0
    for result in results:
        if result['status'] == 'connected':
            expected_time += result.get('wait_time', 0) + idle
        else:
            expected_time += min(result.get('wait_time', max_wait), max_wait) + 1  # +1s pause for failed
    
    print(f"\nExpected total time: ~{expected_time:.0f}s")
    print(f"Actual total time: {total_time:.1f}s")
    
    if abs(total_time - expected_time) < 5:  # 5 second tolerance
        print("✅ PASS: Timing behavior is correct")
    else:
        print("⚠️  WARNING: Timing may be off")

if __name__ == '__main__':
    test_with_timing()