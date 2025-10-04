#!/bin/bash
# Quick setup script for macOS/Linux

echo "================================================"
echo "Phone Test Panel - Localhost Setup"
echo "================================================"

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

$PYTHON_CMD --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup configuration
echo ""
if [ ! -f config.json ]; then
    echo "Creating config.json from template..."
    cp config.example.json config.json
    echo "⚠️  Please edit config.json with your SIP credentials!"
else
    echo "config.json already exists."
fi

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "To start the application:"
echo "1. Edit config.json with your SIP credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo "4. Open: http://localhost:5000"
echo ""