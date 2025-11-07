@echo off
echo Starting Backend Server...
echo.

cd backend

REM Check if venv exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist "..\.env" (
    echo .env file not found. Copying from .env.example...
    copy ..\.env.example ..\.env
    echo Please edit .env file if needed, then restart.
    pause
    exit /b
)

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo Backend will be available at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python main.py

pause

