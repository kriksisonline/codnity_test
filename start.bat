@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo ====================================
echo Codnity Test Project Start Script
echo ====================================
echo.

echo Starting Flask backend...
pushd back
start cmd /k "cd %cd% && call venv\Scripts\activate && python api.py"
popd

echo Starting React frontend...
pushd front
start cmd /k "cd %cd% && npm run dev"
popd

echo Opening browser to frontend...
start "" "localhost:5173"

echo.
echo All servers started.
echo Close terminals to stop the servers.
echo.

pause
