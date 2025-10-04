@echo off
echo ================================
echo Phone Number Test Panel
echo ================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create config.json from example if it doesn't exist
if not exist "config.json" (
    echo Creating config.json from template...
    copy config.example.json config.json
    echo Please edit config.json with your SIP credentials
)

REM Start the application
echo.
echo Starting application...
echo Access the web interface at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ================================

python app.py

pause