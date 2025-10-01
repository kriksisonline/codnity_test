@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo ====================================
echo Codnity Test Project Setup Script
echo ====================================
echo.

echo Setting up Python backend...
pushd back

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

if exist requirements.txt (
    echo Installing Python dependencies...
    call venv\Scripts\activate && pip install -r requirements.txt
) else (
    echo requirements.txt not found, skipping pip install.
)

popd

echo.
echo Setting up React frontend...
pushd front

if exist package.json (
    echo Installing npm packages...
    npm install
) else (
    echo package.json not found.
    exit /b 1
)

popd

echo.
echo Setup complete! 
echo Backend is ready to run: call back\venv\Scripts\activate && python back\api.py
echo Frontend is ready to run: cd front && npm run dev
echo.
