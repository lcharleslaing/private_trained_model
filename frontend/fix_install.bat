@echo off
echo Fixing npm installation issues...
echo.
echo Step 1: Closing any Node processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Cleaning npm cache...
call npm cache clean --force

echo Step 3: Removing node_modules (this may take a moment)...
if exist node_modules (
    echo Please close any file explorers, VS Code, or other programs that might be using these files.
    echo Press any key to continue...
    pause >nul
    rmdir /s /q node_modules 2>nul
)

echo Step 4: Removing package-lock.json...
if exist package-lock.json del package-lock.json

echo Step 5: Installing dependencies (ignoring scripts to avoid patch-package error)...
call npm install --ignore-scripts

echo.
echo Installation complete! You can now run: npm run dev
echo.
pause

