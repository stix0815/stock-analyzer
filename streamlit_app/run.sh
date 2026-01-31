#!/bin/bash

# Stock Analyzer - Quick Start Script
# This script sets up and runs the Streamlit app

echo "======================================"
echo "📊 Stock Analysis App - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 detected"
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Please install pip for Python 3"
    exit 1
fi

echo "✓ pip3 detected"
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    echo "Please run this script from the streamlit_app directory"
    exit 1
fi

echo "✓ Found app.py"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "(This may take a minute the first time)"
echo ""

pip3 install --user -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running quick tests..."
echo ""

python3 test_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Tests failed, but you can still try running the app"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo ""
    echo "✓ All tests passed!"
fi

echo ""
echo "======================================"
echo "🚀 Starting Streamlit App..."
echo "======================================"
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""

# Add Python user bin to PATH for this session
export PATH="$HOME/Library/Python/3.11/bin:$PATH"

# Run Streamlit
python3 -m streamlit run app.py

# If streamlit module not found, try direct command
if [ $? -ne 0 ]; then
    streamlit run app.py
fi
