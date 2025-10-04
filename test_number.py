#!/usr/bin/env python3
"""
Test specific phone number: 63322683000
"""
import requests
import time
import json

# Configuration
BASE_URL = "http://localhost:5000"
TEST_NUMBER = "63322683000"  # Your test number without +

def test_single_number():
    """Test the specific number"""
    print(f"Testing phone number: {TEST_NUMBER}")
    print("=" * 50)
    
    # Start test
    response = requests.post(f"{BASE_URL}/api/test/start", 
                            json={"phone_numbers": [TEST_NUMBER]})
    
    if response.status_code == 200:
        print("✓ Test started successfully")
    else:
        print(f"✗ Failed to start test: {response.text}")
        return
    
    # Monitor progress
    print("\nMonitoring progress...")
    last_status = None
    
    while True:
        response = requests.get(f"{BASE_URL}/api/test/status")
        status = response.json()
        
        if status != last_status:
            print(f"\nStatus Update:")
            print(f"  Running: {status['is_running']}")
            print(f"  Current: {status['current_number']}")
            print(f"  Progress: {status['tested_numbers']}/{status['total_numbers']}")
            print(f"  Connected: {len(status['connected_numbers'])}")
            print(f"  Failed: {len(status['failed_numbers'])}")
            
            if status['connected_numbers']:
                print(f"  Connected Numbers: {status['connected_numbers']}")
            
            last_status = status
        
        if not status['is_running'] and status['tested_numbers'] > 0:
            break
        
        time.sleep(1)
    
    # Get final results
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    response = requests.get(f"{BASE_URL}/api/test/results")
    results = response.json()
    
    for result in results:
        status_icon = "✓" if result['status'] == 'connected' else "✗"
        print(f"{status_icon} {result['phone_number']}: {result['status']} ({result['duration']:.1f}s)")
        if result.get('error'):
            print(f"   Error: {result['error']}")
    
    # Check if our test number connected
    print("\n" + "=" * 50)
    if TEST_NUMBER in status['connected_numbers']:
        print(f"✅ SUCCESS: {TEST_NUMBER} was detected as CONNECTED")
    else:
        print(f"❌ ISSUE: {TEST_NUMBER} was NOT detected as connected")
        print(f"   Status: {results[0]['status'] if results else 'No results'}")

if __name__ == '__main__':
    test_single_number()