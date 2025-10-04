#!/usr/bin/env python3
"""
Fix script for localhost setup issues
"""
import os
import json
import socket
import sys
import subprocess
import platform

def create_config():
    """Create config.json if it doesn't exist"""
    if not os.path.exists('config.json'):
        print("✅ Creating config.json from example...")
        config = {
            "sip": {
                "username": "demo_user",
                "password": "demo_password",
                "server": "pbx.example.com",
                "domain": "pbx.example.com",
                "port": 5060,
                "transport": "UDP",
                "protocol": "SIP"
            },
            "test_settings": {
                "call_duration_seconds": 25,
                "idle_between_calls_seconds": 10,
                "max_concurrent_executions": 0,
                "timeout_seconds": 30,
                "demo_mode": True,
                "demo_numbers": {
                    "connected": ["907086197000", "902161883006", "3698446014"],
                    "failed": ["639758005031"]
                }
            },
            "server": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False
            }
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ config.json created successfully!")
        return config
    else:
        print("ℹ️  config.json already exists")
        with open('config.json', 'r') as f:
            return json.load(f)

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0  # True if port is available

def find_process_on_port(port):
    """Find process using a specific port"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        cmd = f"lsof -i :{port} | grep LISTEN"
    elif system == "Linux":
        cmd = f"lsof -i :{port} | grep LISTEN"
    else:  # Windows
        cmd = f"netstat -ano | findstr :{port}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except:
        return ""

def kill_process_on_port(port):
    """Kill process on specific port"""
    system = platform.system()
    
    if system == "Darwin" or system == "Linux":
        cmd = f"lsof -ti:{port} | xargs kill -9"
    else:  # Windows
        print("On Windows, manually kill the process using Task Manager")
        return False
    
    try:
        subprocess.run(cmd, shell=True)
        return True
    except:
        return False

def fix_port_issue(config):
    """Fix port conflict issues"""
    current_port = config['server']['port']
    
    if not check_port(current_port):
        print(f"\n⚠️  Port {current_port} is already in use!")
        process_info = find_process_on_port(current_port)
        if process_info:
            print(f"Process using port {current_port}:")
            print(process_info)
        
        print("\nOptions:")
        print(f"1. Kill the process on port {current_port}")
        print("2. Use a different port (5001)")
        print("3. Exit and fix manually")
        
        choice = input("\nChoose option (1/2/3): ").strip()
        
        if choice == "1":
            if platform.system() == "Windows":
                print("\nOn Windows, please:")
                print(f"1. Open Task Manager")
                print(f"2. Find the process using port {current_port}")
                print(f"3. End the process")
                print(f"4. Run this script again")
            else:
                print(f"Attempting to kill process on port {current_port}...")
                if kill_process_on_port(current_port):
                    print(f"✅ Port {current_port} cleared!")
                else:
                    print(f"❌ Failed to clear port. Try: sudo lsof -ti:{current_port} | xargs kill -9")
        
        elif choice == "2":
            new_port = 5001
            config['server']['port'] = new_port
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Changed to port {new_port}")
            print(f"📌 Access the app at: http://localhost:{new_port}")
            return new_port
        else:
            sys.exit(0)
    else:
        print(f"✅ Port {current_port} is available!")
    
    return current_port

def main():
    print("🔧 Phone Test Panel - Localhost Fix Script")
    print("=" * 50)
    
    # Step 1: Create/check config.json
    config = create_config()
    
    # Step 2: Fix port issues
    port = fix_port_issue(config)
    
    # Step 3: Final instructions
    print("\n" + "=" * 50)
    print("✅ Setup complete! Now run:")
    print("\n   python app.py")
    print(f"\nThen open: http://localhost:{port}")
    print("\nTest with these numbers:")
    print("  907086197000  (will show as connected)")
    print("  639758005031  (will show as failed)")
    print("  902161883006  (will show as connected)")
    print("  3698446014    (will show as connected)")
    print("=" * 50)

if __name__ == "__main__":
    main()