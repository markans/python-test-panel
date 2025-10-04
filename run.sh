#!/bin/bash

# Phone Number Test Panel - Run Script

echo "================================"
echo "Phone Number Test Panel"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Create config.json from example if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "Creating config.json from template..."
    cp config.example.json config.json
    echo "Please edit config.json with your SIP credentials"
fi

# Start the application
echo ""
echo "Starting application..."
echo "Access the web interface at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

python app.py