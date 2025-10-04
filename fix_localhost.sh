#!/bin/bash

echo "🔧 Phone Test Panel - Localhost Fix Script"
echo "=========================================="

# 1. Create config.json if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "✅ Creating config.json from example..."
    cat > config.json << 'EOF'
{
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
    "demo_mode": true,
    "demo_numbers": {
      "connected": ["907086197000", "902161883006", "3698446014"],
      "failed": ["639758005031"]
    }
  },
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  }
}
EOF
    echo "✅ config.json created successfully!"
else
    echo "ℹ️  config.json already exists"
fi

# 2. Check if port 5000 is in use
echo ""
echo "🔍 Checking port 5000..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is already in use!"
    echo ""
    echo "Options to fix this:"
    echo "1. Kill the process using port 5000:"
    echo "   sudo lsof -ti:5000 | xargs kill -9"
    echo ""
    echo "2. Or use a different port (e.g., 5001):"
    echo "   Edit config.json and change 'port': 5000 to 'port': 5001"
    echo ""
    read -p "Do you want to kill the process on port 5000? (y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        sudo lsof -ti:5000 | xargs kill -9 2>/dev/null
        echo "✅ Port 5000 cleared!"
    else
        echo "Changing to port 5001..."
        sed -i.bak 's/"port": 5000/"port": 5001/' config.json
        echo "✅ Changed to port 5001. Access the app at http://localhost:5001"
    fi
else
    echo "✅ Port 5000 is available!"
fi

echo ""
echo "🎯 Ready to start! Run:"
echo "   python app.py"
echo ""
echo "Then open: http://localhost:5000 (or :5001 if changed)"
echo "=========================================="