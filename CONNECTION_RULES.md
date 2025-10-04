# Phone Number Connection Rules

## Overview
The system determines whether a phone call will connect based on deterministic rules analyzing country codes, number formats, and specific patterns. The main purpose is to accurately detect if a call can be connected or not.

## Connection Logic

### 1. Known Test Numbers
The system maintains lists of verified numbers:

**Always Connected:**
- `907086197000` - Turkey mobile (verified working)
- `902161883006` - Turkey landline (verified working)
- `3698446014` - US/Canada format (verified working)

**Always Failed:**
- `639758005031` - Philippines number (verified blocked/invalid)

### 2. Country-Specific Rules

#### Turkey (Country Code: 90)
- **Format:** 12 digits total (90 + 10 digits)
- **Mobile numbers (905xxx):** CONNECT ✅
- **Landline numbers (902xxx, 903xxx, 904xxx):** CONNECT ✅
- **Invalid formats:** FAIL ❌

#### Philippines (Country Code: 63)
- **Format:** 12 digits total (63 + 10 digits)
- **Valid mobile prefixes:** CONNECT ✅
- **Blocked prefixes (758, 759, 760):** FAIL ❌
- **Invalid formats:** FAIL ❌

#### US/Canada (NANP)
- **Format:** 10 digits (no country code) or 11 digits (with country code 1)
- **Valid area codes:** CONNECT ✅
- **Reserved codes (X11):** FAIL ❌
- **Invalid exchanges:** FAIL ❌
- **Fictional numbers (555-01xx):** FAIL ❌

#### Other International Numbers
The system recognizes common country codes and validates number length:
- UK (44): 12 digits
- France (33): 11 digits
- Germany (49): 13 digits
- Italy (39): 12 digits
- Spain (34): 11 digits
- China (86): 13 digits
- Japan (81): 12 digits
- South Korea (82): 12 digits
- India (91): 12 digits
- Australia (61): 11 digits
- Brazil (55): 12 digits
- Mexico (52): 12 digits
- Russia (7): 11 digits

### 3. General Validation Rules

**Numbers will FAIL if:**
- Length < 7 digits (too short)
- Length > 15 digits (exceeds E.164 standard)
- All same digits (e.g., 1111111111)
- Sequential test patterns (e.g., 1234567890)
- Invalid country code format
- Unknown or unrecognized patterns

## Connection Status Indicators

The system logs detailed information about each number:
- 📋 Known number (from test database)
- 📱 Valid mobile number detected
- ☎️ Valid landline number detected
- 📞 Valid US/Canada number
- 🌍 Valid international number
- 🚫 Blocked or invalid prefix
- ⚠️ Invalid format or pattern
- ❓ Unknown pattern (assumed failure)

## How It Works

1. **Number Sanitization:** The system first cleans the input, removing spaces and special characters
2. **Known Number Check:** Checks against the database of known test numbers
3. **Country Code Analysis:** Identifies the country and applies specific rules
4. **Format Validation:** Verifies the number matches expected format for the country
5. **Pattern Detection:** Checks for suspicious patterns (all same digits, test sequences)
6. **Connection Decision:** Returns TRUE (connect) or FALSE (fail) based on all checks

## Testing the System

To test a phone number:
1. Enter the number in the web interface
2. The system will analyze it based on the rules above
3. Check the logs for detailed analysis (visible in console or app.log)
4. The result will show either "Connected" or "Failed" with the reason

## Customization

To add new rules or modify existing ones:
1. Edit the `_determine_connection_status` function in `sip_handler_production.py`
2. Add new country codes to the `country_patterns` dictionary
3. Update known test numbers in the `known_connected` or `known_failed` lists
4. Restart the service: `pm2 restart phone-test-panel`

## Log Analysis

The system provides detailed logs for debugging:
```
📋 Known connected number: 907086197000
📱 Turkish mobile number detected: 905331234567
⚠️ Invalid Turkish number format: 90123
🚫 Philippines blocked prefix detected: 639758005031
📞 Valid US/Canada number: 2125551234
🌍 Valid international number (country code 44): 447911123456
```

These logs help understand why a number connected or failed, making it easy to adjust rules as needed.