#!/usr/bin/env python3
"""
Test script to validate the setup
"""
import sys
import json

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported")
        import flask_socketio
        print("✓ Flask-SocketIO imported")
        import openpyxl
        print("✓ openpyxl imported")
        import eventlet
        print("✓ eventlet imported")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test if configuration file exists and is valid"""
    print("\nTesting configuration...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✓ config.json found and valid")
        
        # Check required fields
        if 'sip' in config:
            print(f"✓ SIP config found - User: {config['sip']['username']}")
        else:
            print("✗ SIP configuration missing")
            return False
        
        return True
    except FileNotFoundError:
        print("✗ config.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in config.json: {e}")
        return False

def test_sip_handler():
    """Test if SIP handler can be initialized"""
    print("\nTesting SIP handler...")
    try:
        from sip_handler_simple import SimpleSIPTester
        tester = SimpleSIPTester()
        print("✓ SIP handler initialized")
        
        status = tester.get_status()
        print(f"✓ Status retrieved: Running={status['is_running']}")
        return True
    except Exception as e:
        print(f"✗ SIP handler error: {e}")
        return False

def test_export():
    """Test export utilities"""
    print("\nTesting export utilities...")
    try:
        from export_utils import export_to_csv, export_to_excel
        print("✓ Export utilities imported")
        
        # Test with sample data
        test_results = [
            {
                'phone_number': '+1234567890',
                'status': 'connected',
                'timestamp': '2024-01-01T12:00:00',
                'duration': 25.0,
                'error': None
            }
        ]
        
        # Test CSV export
        csv_file = export_to_csv(test_results, 'test_export.csv')
        print(f"✓ CSV export tested: {csv_file}")
        
        # Test Excel export
        xlsx_file = export_to_excel(test_results, 'test_export.xlsx')
        print(f"✓ Excel export tested: {xlsx_file}")
        
        # Clean up test files
        import os
        os.remove('test_export.csv')
        os.remove('test_export.xlsx')
        
        return True
    except Exception as e:
        print(f"✗ Export error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("Phone Number Test Panel - Setup Validation")
    print("="*50)
    
    all_pass = True
    
    if not test_imports():
        all_pass = False
    
    if not test_config():
        all_pass = False
    
    if not test_sip_handler():
        all_pass = False
    
    if not test_export():
        all_pass = False
    
    print("\n" + "="*50)
    if all_pass:
        print("✓ All tests passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nOr use the convenience script:")
        print("  ./run.sh (Linux/Mac)")
        print("  run.bat (Windows)")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()