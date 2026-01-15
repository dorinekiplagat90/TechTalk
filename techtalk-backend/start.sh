#!/bin/bash

echo "🚀 Starting TechTalk Backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Seed database if it doesn't exist
if [ ! -f "techtalk.db" ]; then
    echo "Seeding database..."
    python seed.py
fi

# Start server
echo "Starting FastAPI server on http://localhost:8000"
uvicorn main:app --reload
