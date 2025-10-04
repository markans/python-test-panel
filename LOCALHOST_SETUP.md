# 🏠 Phone Test Panel - Localhost Setup Guide

## 📥 Quick Start for Localhost

### 1. Clone the Repository
```bash
git clone https://github.com/markans/python-test-panel.git
cd python-test-panel
```

### 2. Set Up Python Environment
```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Application
```bash
# Copy example config if config.json doesn't exist
cp config.example.json config.json

# Edit config.json if needed (default settings work for demo)
```

### 4. Run the Application
```bash
# Simple method:
python app.py

# Or using the provided scripts:
# On Linux/Mac:
./run.sh
# On Windows:
run.bat
```

### 5. Access the Application
Open your browser and go to:
```
http://localhost:5000
```

## 🧪 Testing the Demo Numbers

### Via Web Interface:
1. Open http://localhost:5000 in your browser
2. Enter these test numbers in the text area:
```
907086197000
639758005031
902161883006
3698446014
```
3. Click "Start Test"

### Expected Results:
- ✅ `907086197000` - Connected
- ❌ `639758005031` - Failed  
- ✅ `902161883006` - Connected
- ✅ `3698446014` - Connected

### Via Test Scripts:
```bash
# Test demo numbers
python test_demo_numbers.py

# Run comprehensive test
python test_final_demo.py

# Test stats reset functionality
python test_stats_reset.py
```

## 📋 Configuration Details

The `config.json` file contains:

```json
{
  "sip": {
    "username": "your_sip_username",
    "password": "your_sip_password",
    "server": "pbx.example.com",
    "domain": "pbx.example.com",
    "port": 5060
  },
  "test_settings": {
    "call_duration_seconds": 25,
    "idle_between_calls_seconds": 10,
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
```

**Note**: Demo mode is enabled by default. The demo numbers will always return predefined results for testing purposes.

## 🔧 Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
# Edit config.json to change port:
"server": {
  "port": 5001  # Change to different port
}
```

### Dependencies Installation Issues
```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies one by one if needed
pip install Flask==2.3.3
pip install flask-socketio==5.3.4
pip install python-socketio==5.9.0
pip install eventlet==0.33.3
pip install openpyxl==3.1.2
```

### Permission Issues on Linux/Mac
```bash
# Make run script executable
chmod +x run.sh

# Run with proper permissions
./run.sh
```

## 📦 Required Dependencies

- Python 3.7+
- Flask 2.3.3
- Flask-SocketIO 5.3.4
- python-socketio 5.9.0
- eventlet 0.33.3
- openpyxl 3.1.2

## 🎯 Features Working in Localhost

✅ **Demo Numbers** - Test numbers return expected results
✅ **Stats Reset** - Statistics reset when starting new tests
✅ **Real-time Updates** - WebSocket updates work locally
✅ **Export Functions** - CSV/Excel export works
✅ **Number Format Support** - Various formats handled correctly

## 📊 API Endpoints (Localhost)

- **Status**: http://localhost:5000/api/test/status
- **Start Test**: POST http://localhost:5000/api/test/start
- **Results**: http://localhost:5000/api/test/results
- **Export CSV**: http://localhost:5000/api/export/csv
- **Export Excel**: http://localhost:5000/api/export/xlsx

## 💡 Development Tips

1. **Watch Logs**: The application prints detailed logs in the terminal
2. **Debug Mode**: Set `"debug": true` in config.json for detailed error messages
3. **Test Scripts**: Use the provided test scripts to verify functionality
4. **Browser Console**: Check browser console for WebSocket connection status

## ✅ Verification Checklist

After setup, verify everything works:
- [ ] Application starts without errors
- [ ] Web interface loads at http://localhost:5000
- [ ] Demo numbers test shows correct results
- [ ] Stats reset when starting new test
- [ ] Real-time logs appear in the interface
- [ ] Export functions work (CSV/Excel)

---
**Repository**: https://github.com/markans/python-test-panel
**Issues/Questions**: Please create an issue on GitHub