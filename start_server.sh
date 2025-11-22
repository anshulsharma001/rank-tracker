#!/bin/bash
# Start script for Google Rank Tracker Web Interface

echo "============================================================"
echo "Starting Google Rank Tracker Web Interface"
echo "============================================================"
echo ""
echo "Checking setup..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Make sure to configure your API keys"
fi

# Check if credentials.json exists (needed for Google Docs/Sheets)
if [ ! -f credentials.json ]; then
    echo "⚠️  Warning: credentials.json not found"
    echo "   Google Docs/Sheets storage may not work without credentials"
fi

echo ""
echo "Starting web server..."
echo "Open your browser and go to: http://localhost:8080"
echo ""
echo "Note: Using port 8080 (ports 5000/5001 are often used by AirPlay on macOS)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 app.py

