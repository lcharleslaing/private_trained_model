#!/bin/bash

echo "Starting Frontend Development Server (UI Preview)..."
echo
echo "Note: Backend and Ollama are not required to view the interface"
echo

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo
echo "Starting Vite dev server..."
echo "Frontend will be available at http://localhost:5173"
echo
echo "The interface will load, but chat functionality requires:"
echo "- Backend server running (python backend/main.py)"
echo "- Ollama installed and running"
echo "- Model downloaded (ollama pull llama3.2)"
echo
echo "Press Ctrl+C to stop the server"
echo

npm run dev

