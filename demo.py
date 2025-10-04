#!/usr/bin/env python3
"""
Demo script to show how the phone testing works
"""
import time
from sip_handler_simple import SimpleSIPTester

def demo_callback(status):
    """Status callback for demo"""
    print(f"\n[STATUS UPDATE]")
    print(f"  Running: {status['is_running']}")
    print(f"  Progress: {status['tested_numbers']}/{status['total_numbers']}")
    print(f"  Current: {status['current_number']}")
    print(f"  Connected: {len(status['connected_numbers'])}")
    print(f"  Failed: {len(status['failed_numbers'])}")

def log_callback(log):
    """Log callback for demo"""
    print(f"[{log['timestamp']}] {log['level'].upper()}: {log['message']}")

def main():
    """Run demo"""
    print("="*60)
    print("Phone Number Test Panel - Demo Mode")
    print("="*60)
    print("\nThis demo will test sample phone numbers using the configured")
    print("SIP account. The actual connectivity will depend on your PBX.")
    print("-"*60)
    
    # Initialize tester
    tester = SimpleSIPTester()
    
    # Sample phone numbers to test
    test_numbers = [
        "+1234567890",  # Sample US number
        "+447700900000",  # Sample UK number
        "+33612345678",  # Sample France number
    ]
    
    print(f"\nTesting {len(test_numbers)} phone numbers:")
    for num in test_numbers:
        print(f"  • {num}")
    
    print("\nStarting test...")
    print("-"*60)
    
    # Run test
    tester.test_multiple_numbers(
        test_numbers,
        status_callback=demo_callback,
        log_callback=log_callback
    )
    
    # Wait for completion
    while tester.get_status()['is_running']:
        time.sleep(1)
    
    # Show results
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    results = tester.get_results()
    for result in results:
        status_icon = "✓" if result['status'] == 'connected' else "✗"
        print(f"{status_icon} {result['phone_number']}: {result['status']} "
              f"({result['duration']:.1f}s)")
    
    # Summary
    status = tester.get_status()
    print("\n" + "-"*60)
    print(f"Total tested: {status['tested_numbers']}")
    print(f"Connected: {len(status['connected_numbers'])}")
    print(f"Failed: {len(status['failed_numbers'])}")
    
    if status['connected_numbers']:
        print(f"\nConnected numbers:")
        for num in status['connected_numbers']:
            print(f"  • {num}")

if __name__ == '__main__':
    main()