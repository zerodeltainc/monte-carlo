#!/bin/bash
# Quick Start Script for Trade Simulator

echo "🚀 Starting Trade Simulator..."
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Launching Streamlit app..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py
