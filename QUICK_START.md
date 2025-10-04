# 🚀 Phone Test Panel - Quick Start

## GitHub Repository
📦 **Repository**: https://github.com/markans/python-test-panel

## Quick Setup Commands

### Windows Users:
```bash
git clone https://github.com/markans/python-test-panel.git
cd python-test-panel
setup_localhost.bat
```

### macOS/Linux Users:
```bash
git clone https://github.com/markans/python-test-panel.git
cd python-test-panel
chmod +x setup_localhost.sh
./setup_localhost.sh
```

## Manual Setup (All Platforms)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/markans/python-test-panel.git
   cd python-test-panel
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure SIP:**
   ```bash
   cp config.example.json config.json
   # Edit config.json with your SIP credentials
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```

7. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Test Numbers (Working Examples)

These numbers are confirmed to work with the current logic:

✅ **Connected:**
- `907086197000` - Turkey mobile
- `902161883006` - Turkey landline
- `3698446014` - US/Canada format

❌ **Failed:**
- `639758005031` - Philippines (blocked prefix)

## Key Features

- ✅ Deterministic connection detection (no random results)
- 🌍 International number validation (14+ countries)
- 📊 Real-time status updates via WebSocket
- 💾 Export results to CSV/Excel
- 📝 Detailed logging with connection reasons

## Need Help?

- 📖 Full setup guide: [LOCALHOST_SETUP_GUIDE.md](LOCALHOST_SETUP_GUIDE.md)
- 📋 Connection rules: [CONNECTION_RULES.md](CONNECTION_RULES.md)
- 🧪 Test the logic: Run `python test_connection_rules.py`

## Current Service Status

🟢 **Running at**: https://5000-ijlq5n3jues9w0twmc5tr-6532622b.e2b.dev

---
Last updated: 2025-10-04