# 🚀 Localhost Setup Guide

This guide will help you run the Phone Test Panel on your local machine.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.7 or higher installed
- Git installed
- pip (Python package manager)
- A terminal/command prompt

## 🔧 Installation Steps

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/markans/python-test-panel.git
cd python-test-panel
```

### Step 2: Create Virtual Environment (Recommended)

This keeps your project dependencies isolated:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-SocketIO (real-time communication)
- openpyxl (Excel export)
- eventlet (async support)

### Step 4: Configure SIP Account

1. Copy the example configuration:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your SIP credentials:
```json
{
    "sip": {
        "username": "your_sip_username",
        "password": "your_sip_password",
        "server": "your.sip.server.com",
        "port": 5060,
        "realm": "your.sip.server.com",
        "from_domain": "your.sip.server.com"
    },
    "test_settings": {
        "call_duration_seconds": 25,
        "idle_between_calls_seconds": 10,
        "max_concurrent": 1
    }
}
```

### Step 5: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 6: Access the Web Interface

Open your web browser and go to:
```
http://localhost:5000
```

## 🖥️ Using the Application

### Testing Phone Numbers

1. **Enter phone numbers** in the text area (one per line):
   ```
   907086197000
   639758005031
   902161883006
   3698446014
   +12125551234
   ```

2. **Adjust timing settings** if needed:
   - Max Wait: How long to wait for connection (default: 25 seconds)
   - Idle Time: Pause between calls (default: 10 seconds)

3. **Click "Start Test"** to begin testing

4. **Monitor progress**:
   - Real-time status updates show current number being tested
   - Log panel displays detailed connection information
   - Progress bar shows overall completion

5. **Export results**:
   - Click "Export to CSV" for spreadsheet format
   - Click "Export to Excel" for formatted Excel file
   - Click "Export Connected Only" for just successful numbers

### Understanding Results

The system will show for each number:
- ✅ **Connected**: Number successfully connected based on validation rules
- ❌ **Failed**: Number failed due to invalid format, blocked prefix, or other rules

Check the logs for detailed reasons:
- 📋 Known test number
- 📱 Valid mobile number
- ☎️ Valid landline number
- 🚫 Blocked or invalid prefix
- ⚠️ Invalid format
- 🌍 International number detected

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Port 5000 Already in Use
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID_NUMBER>
```

Or change the port in `app.py`:
```python
socketio.run(app, host='127.0.0.1', port=5001, debug=True)
```

#### 2. Module Import Errors
Make sure virtual environment is activated and all dependencies installed:
```bash
pip install --upgrade -r requirements.txt
```

#### 3. Permission Denied (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

#### 4. SIP Connection Issues
- Verify your SIP credentials in `config.json`
- Check firewall settings (port 5060 for SIP)
- Ensure your SIP account is active

## 🛠️ Advanced Configuration

### Using Different Python Version
If you have multiple Python versions:
```bash
# Windows
py -3.9 -m venv venv

# macOS/Linux
python3.9 -m venv venv
```

### Running with PM2 (Process Manager)
For production-like setup with auto-restart:

1. Install Node.js and PM2:
```bash
npm install -g pm2
```

2. Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'phone-test-panel',
    script: 'app.py',
    interpreter: 'python3',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
  }]
}
```

3. Start with PM2:
```bash
pm2 start ecosystem.config.js
pm2 logs phone-test-panel
```

### Running on Different Network Interface
To make accessible from other devices on your network:

```python
# In app.py, change:
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

Then access via your computer's IP address:
```
http://192.168.1.100:5000  # Replace with your IP
```

## 📁 Project Structure

```
python-test-panel/
├── app.py                      # Main Flask application
├── sip_handler_production.py   # Production SIP handler with connection logic
├── export_utils.py             # Export functionality
├── config.json                 # Your SIP configuration (create from example)
├── config.example.json         # Configuration template
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface
├── static/                    # Static files (created automatically)
├── CONNECTION_RULES.md        # Detailed connection rules documentation
├── test_connection_rules.py   # Test suite for validation logic
└── README.md                  # Main documentation
```

## 🔒 Security Notes

1. **Never commit `config.json`** with real credentials to Git
2. **Use environment variables** for production:
   ```python
   import os
   sip_username = os.environ.get('SIP_USERNAME')
   ```
3. **Restrict network access** in production environments
4. **Use HTTPS** with proper certificates for production

## 📞 Connection Rules

The system uses deterministic rules to validate phone numbers:
- **Turkey (90)**: Validates mobile and landline formats
- **Philippines (63)**: Checks network prefixes, blocks specific ranges
- **US/Canada**: Validates NANP format, detects fictional numbers
- **International**: Supports 14+ countries with proper validation

See [CONNECTION_RULES.md](CONNECTION_RULES.md) for detailed information.

## 🆘 Getting Help

If you encounter issues:
1. Check the logs in the terminal
2. Review the [CONNECTION_RULES.md](CONNECTION_RULES.md) for validation logic
3. Ensure all dependencies are installed correctly
4. Verify your Python version: `python --version`

## 🎉 Quick Start Summary

```bash
# Clone and enter directory
git clone https://github.com/markans/python-test-panel.git
cd python-test-panel

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure SIP
cp config.example.json config.json
# Edit config.json with your credentials

# Run
python app.py

# Open browser
# Go to http://localhost:5000
```

Your Phone Test Panel should now be running locally! 🚀