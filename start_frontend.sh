#!/bin/bash

echo "Starting Frontend Development Server..."
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
echo "Press Ctrl+C to stop the server"
echo

npm run dev

