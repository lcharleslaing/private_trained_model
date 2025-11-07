#!/bin/bash

echo "Starting Backend Server..."
echo

cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f "../.env" ]; then
    echo ".env file not found. Copying from .env.example..."
    cp ../.env.example ../.env
    echo "Please edit .env file if needed, then restart."
    exit 1
fi

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Starting FastAPI server..."
echo "Backend will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo

python main.py

