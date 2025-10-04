#!/usr/bin/env python3
"""
Test script to verify the connection rules logic
"""
from sip_handler_production import ProductionSIPTester

def test_connection_rules():
    """Test various phone numbers against the connection rules"""
    
    # Initialize the tester
    tester = ProductionSIPTester()
    
    # Test cases: (number, expected_result, description)
    test_cases = [
        # Known test numbers
        ("907086197000", True, "Known connected - Turkey mobile"),
        ("902161883006", True, "Known connected - Turkey landline"),
        ("3698446014", True, "Known connected - US/Canada format"),
        ("639758005031", False, "Known failed - Philippines"),
        
        # Turkish numbers
        ("905331234567", True, "Turkey mobile - should connect"),
        ("902121234567", True, "Turkey landline - should connect"),
        ("908881234567", False, "Turkey invalid prefix - should fail"),
        ("90123", False, "Turkey too short - should fail"),
        
        # Philippines numbers
        ("639171234567", True, "Philippines valid mobile - should connect"),
        ("639758999999", False, "Philippines blocked prefix - should fail"),
        ("639991234567", True, "Philippines valid prefix - should connect"),
        ("63123", False, "Philippines too short - should fail"),
        
        # US/Canada numbers
        ("2125551234", True, "US New York number - should connect"),
        ("4165551234", True, "Canada Toronto number - should connect"),
        ("5555550100", False, "US fictional number - should fail"),
        ("9115551234", False, "US invalid area code - should fail"),
        ("12125551234", True, "US with country code - should connect"),
        
        # International numbers
        ("447911123456", True, "UK mobile - should connect"),
        ("33612345678", True, "France number - should connect"),
        ("8613912345678", True, "China mobile - should connect"),
        ("819012345678", True, "Japan mobile - should connect"),
        
        # Invalid patterns
        ("1111111111", False, "All same digits - should fail"),
        ("1234567890", False, "Sequential pattern - should fail"),
        ("123", False, "Too short - should fail"),
        ("1234567890123456", False, "Too long - should fail"),
    ]
    
    print("=" * 80)
    print("PHONE NUMBER CONNECTION RULES TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for number, expected, description in test_cases:
        # Clean the number
        clean_num = tester._sanitize_number(number)
        
        # Test the connection logic
        result = tester._determine_connection_status(clean_num)
        
        # Check if it matches expected
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        # Print result
        print(f"{status} | {number:20} | Expected: {str(expected):5} | Got: {str(result):5} | {description}")
    
    print("=" * 80)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    if failed == 0:
        print("🎉 All tests passed successfully!")
    else:
        print(f"⚠️ {failed} tests failed. Please review the connection logic.")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = test_connection_rules()
    sys.exit(0 if success else 1)