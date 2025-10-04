@echo off
REM Quick setup script for Windows

echo ================================================
echo Phone Test Panel - Localhost Setup
echo ================================================

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Setup configuration
echo.
if not exist config.json (
    echo Creating config.json from template...
    copy config.example.json config.json
    echo WARNING: Please edit config.json with your SIP credentials!
) else (
    echo config.json already exists.
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To start the application:
echo 1. Edit config.json with your SIP credentials
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python app.py
echo 4. Open: http://localhost:5000
echo.
pause