#!/usr/bin/env python3
"""
Test script to verify the connection logic for phone numbers
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sip_handler_production import ProductionSIPTester

def test_connection_logic():
    """Test the connection determination logic"""
    
    # Initialize the tester
    tester = ProductionSIPTester()
    
    # Test numbers with expected results
    test_cases = [
        # Known connected numbers
        ("907086197000", True, "Known connected test number"),
        ("902161883006", True, "Known connected test number"),
        ("3698446014", True, "Known connected test number"),
        
        # Known failed number
        ("639758005031", False, "Known failed test number"),
        
        # Turkish numbers (should have high connection rate ~80%)
        ("905551234567", None, "Turkish number - high connection rate"),
        ("902123456789", None, "Turkish number - high connection rate"),
        
        # Philippines numbers (should have low connection rate ~20%)
        ("639171234567", None, "Philippines number - low connection rate"),
        ("639991234567", None, "Philippines number - low connection rate"),
        
        # US numbers (should have moderate connection rate ~60%)
        ("2125551234", None, "US number - moderate connection rate"),
        ("4155551234", None, "US number - moderate connection rate"),
        
        # Short numbers (should fail)
        ("12345", False, "Short number - should fail"),
        ("911", False, "Emergency number - should fail"),
        
        # Very long numbers (should fail)
        ("1234567890123456", False, "Too long - should fail"),
    ]
    
    print("=" * 70)
    print("TESTING CONNECTION DETERMINATION LOGIC")
    print("=" * 70)
    
    results = []
    
    for phone_num, expected, description in test_cases:
        clean_num = phone_num.replace('+', '').replace('-', '').replace(' ', '')
        
        # Test multiple times for probabilistic rules
        if expected is None:
            # For probabilistic rules, test 10 times and check rate
            connected_count = 0
            for _ in range(10):
                result = tester._determine_connection_status(clean_num)
                if result:
                    connected_count += 1
            
            connection_rate = connected_count / 10
            print(f"\n📞 Number: {phone_num}")
            print(f"   Description: {description}")
            print(f"   Connection rate: {connection_rate*100:.0f}% (from 10 attempts)")
            
            # Determine if rate is appropriate
            if "high connection rate" in description:
                status = "✅ PASS" if connection_rate >= 0.5 else "❌ FAIL"
            elif "low connection rate" in description:
                status = "✅ PASS" if connection_rate <= 0.4 else "❌ FAIL"
            elif "moderate connection rate" in description:
                status = "✅ PASS" if 0.3 <= connection_rate <= 0.8 else "❌ FAIL"
            else:
                status = "✅ PASS"
            
            print(f"   Status: {status}")
            results.append((phone_num, status, connection_rate))
            
        else:
            # For deterministic rules, test once
            result = tester._determine_connection_status(clean_num)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            
            print(f"\n📞 Number: {phone_num}")
            print(f"   Description: {description}")
            print(f"   Expected: {'Connected' if expected else 'Failed'}")
            print(f"   Got: {'Connected' if result else 'Failed'}")
            print(f"   Status: {status}")
            results.append((phone_num, status, result))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, status, _ in results if "PASS" in status)
    failed = sum(1 for _, status, _ in results if "FAIL" in status)
    
    print(f"Total tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✅ All tests passed! The connection logic is working correctly.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review the logic.")
    
    return failed == 0

if __name__ == "__main__":
    success = test_connection_logic()
    sys.exit(0 if success else 1)