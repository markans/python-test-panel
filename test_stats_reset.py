#!/usr/bin/env python3
"""
Test script to verify that stats reset properly when starting a new test
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_stats_reset():
    print("Testing Stats Reset Functionality")
    print("="*50)
    
    # First test with 2 numbers
    print("\n1. First Test (2 numbers)")
    test1_numbers = ["907086197000", "639758005031"]
    
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test1_numbers,
        "max_wait_seconds": 10,
        "idle_seconds": 2
    })
    
    if response.status_code != 200:
        print(f"Failed to start first test: {response.text}")
        return
    
    print("First test started...")
    
    # Wait for first test to complete
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        if not status['is_running']:
            break
        time.sleep(0.5)
    
    # Check final stats from first test
    print(f"First test results:")
    print(f"  Total: {status['total_numbers']}")
    print(f"  Tested: {status['tested_numbers']}")
    print(f"  Connected: {len(status['connected_numbers'])}")
    print(f"  Failed: {len(status['failed_numbers'])}")
    
    # Give a small pause
    time.sleep(2)
    
    # Start second test with different numbers
    print("\n2. Second Test (2 different numbers)")
    test2_numbers = ["902161883006", "3698446014"]
    
    # Check status immediately before starting second test
    response = requests.get(f"{BASE_URL}/api/test/status")
    pre_status = response.json()
    print(f"\nStatus BEFORE starting second test:")
    print(f"  Total: {pre_status['total_numbers']}")
    print(f"  Tested: {pre_status['tested_numbers']}")
    print(f"  Connected: {len(pre_status['connected_numbers'])}")
    print(f"  Failed: {len(pre_status['failed_numbers'])}")
    
    # Start second test
    response = requests.post(f"{BASE_URL}/api/test/start", json={
        "phone_numbers": test2_numbers,
        "max_wait_seconds": 10,
        "idle_seconds": 2
    })
    
    if response.status_code != 200:
        print(f"Failed to start second test: {response.text}")
        return
    
    print("\nSecond test started...")
    
    # Check status immediately after starting second test
    response = requests.get(f"{BASE_URL}/api/test/status")
    immediate_status = response.json()
    print(f"\nStatus IMMEDIATELY AFTER starting second test:")
    print(f"  Total: {immediate_status['total_numbers']}")
    print(f"  Tested: {immediate_status['tested_numbers']}")
    print(f"  Connected: {len(immediate_status['connected_numbers'])}")
    print(f"  Failed: {len(immediate_status['failed_numbers'])}")
    
    # Verify stats were reset
    if immediate_status['tested_numbers'] == 0 and \
       len(immediate_status['connected_numbers']) == 0 and \
       len(immediate_status['failed_numbers']) == 0 and \
       immediate_status['total_numbers'] == 2:
        print("\n✅ SUCCESS: Stats were properly reset to 0!")
    else:
        print("\n❌ FAILURE: Stats were not reset properly!")
    
    # Wait for second test to complete
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        if not status['is_running']:
            break
        time.sleep(0.5)
    
    # Check final stats from second test
    print(f"\nSecond test final results:")
    print(f"  Total: {status['total_numbers']}")
    print(f"  Tested: {status['tested_numbers']}")
    print(f"  Connected: {len(status['connected_numbers'])}")
    print(f"  Failed: {len(status['failed_numbers'])}")
    
    # Final verification
    print("\n" + "="*50)
    print("Verification:")
    if status['tested_numbers'] == 2 and len(status['connected_numbers']) == 2:
        print("✅ Stats properly reflect only the second test results")
    else:
        print("❌ Stats do not match expected results")

if __name__ == '__main__':
    time.sleep(1)
    test_stats_reset()