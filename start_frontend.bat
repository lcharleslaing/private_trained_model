@echo off
echo Starting Frontend Development Server...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo.
echo Starting Vite dev server...
echo Frontend will be available at http://localhost:5173
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause

