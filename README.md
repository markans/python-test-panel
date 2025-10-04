# Phone Number Test Panel

A lightweight web-based application for testing phone number connectivity using SIP protocol. This tool allows you to batch test multiple phone numbers to identify which ones are connected/reachable.

## Features

- ✅ **Batch Testing**: Test multiple phone numbers sequentially
- 📊 **Real-time Status**: Live updates and progress tracking via WebSocket
- 📝 **Detailed Logging**: Real-time log display with color-coded messages
- 💾 **Export Results**: Export results to CSV or Excel format
- 🔧 **Configurable Settings**: Easy SIP account configuration through web interface
- ⏱️ **Customizable Timing**: 25-second call duration, 10-second idle between calls
- 🎯 **Minimal Dependencies**: Uses lightweight Python libraries

## Project Structure

```
phone-test-panel/
├── app.py                  # Main Flask application
├── sip_handler_simple.py   # Simplified SIP call handler
├── export_utils.py         # CSV/Excel export utilities
├── config.example.json     # Configuration template
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
└── README.md              # Documentation
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd phone-test-panel
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure SIP account**

Copy the example configuration:
```bash
cp config.example.json config.json
```

Edit `config.json` with your SIP credentials:
```json
{
    "sip": {
        "username": "your_username",
        "password": "your_password",
        "server": "your_pbx_server",
        "domain": "your_pbx_domain",
        "port": 5060,
        "transport": "UDP",
        "protocol": "SIP"
    }
}
```

## Usage

### Starting the Application

1. **Run the application**
```bash
python app.py
```

2. **Open web browser**
Navigate to: `http://localhost:5000`

### Testing Phone Numbers

1. **Configure SIP Settings**
   - Enter your SIP credentials in the configuration panel
   - Click "Save Configuration"

2. **Enter Phone Numbers**
   - Input phone numbers in the text area (one per line)
   - Format: Include country code (e.g., +1234567890)

3. **Start Testing**
   - Click "Start Test" button
   - Monitor progress in real-time
   - View logs for each number tested

4. **Export Results**
   - Click "Export CSV" for comma-separated values
   - Click "Export Excel" for formatted spreadsheet
   - Click "Export Connected Only" for successful numbers only

### Test Behavior

- **Call Duration**: Each connected call lasts 25 seconds
- **Idle Time**: 10-second pause between calls
- **Timeout**: 30-second timeout for connection attempts
- **Max Executions**: No limit (processes all numbers sequentially)

## API Endpoints

- `GET /` - Main web interface
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `POST /api/test/start` - Start phone number testing
- `POST /api/test/stop` - Stop current test
- `GET /api/test/status` - Get current test status
- `GET /api/test/results` - Get test results
- `GET /api/export/<format>` - Export results (csv/xlsx)

## WebSocket Events

- `connect` - Client connected
- `status_update` - Test status update
- `log_update` - New log entry

## Configuration Options

### SIP Settings
- `username`: SIP account username
- `password`: SIP account password
- `server`: PBX server address
- `domain`: SIP domain
- `port`: SIP port (default: 5060)
- `transport`: Transport protocol (UDP)

### Test Settings
- `call_duration_seconds`: Duration of each call (25s)
- `idle_between_calls_seconds`: Pause between calls (10s)
- `max_concurrent_executions`: Concurrent calls (0 = sequential)
- `timeout_seconds`: Connection timeout (30s)

## Export Formats

### CSV Export
- Phone number
- Status (connected/failed/timeout/error)
- Timestamp
- Duration
- Error details (if any)

### Excel Export
- Detailed results sheet with formatting
- Summary sheet with statistics
- Connected numbers list
- Color-coded status indicators

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify SIP credentials are correct
   - Check network connectivity to PBX server
   - Ensure firewall allows UDP port 5060

2. **No Results Export**
   - Complete at least one test before exporting
   - Check write permissions in application directory

3. **WebSocket Connection Error**
   - Ensure port 5000 is not blocked
   - Try refreshing the browser page

### Logging

Application logs are displayed in:
- Web interface (real-time log panel)
- Console output (terminal where app.py is running)

## Security Notes

- SIP passwords are stored in local config.json
- Use `.gitignore` to exclude config.json from version control
- Run application on localhost for local testing
- Use HTTPS and proper authentication for production deployment

## Limitations

- Sequential testing only (no parallel calls)
- Basic SIP implementation (may not support all PBX systems)
- UDP transport only
- No audio streaming (connection test only)

## Requirements

- Python 3.7+
- Flask 3.0.0
- Flask-SocketIO 5.3.5
- python-socketio 5.10.0
- openpyxl 3.1.2
- eventlet 0.33.3

## License

This project is provided as-is for testing purposes.

## Support

For issues or questions, please check the logs for error messages and ensure your SIP configuration is correct.