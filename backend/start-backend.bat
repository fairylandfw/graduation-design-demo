@echo off
title Backend Service
cd /d "%~dp0"

echo Starting Backend Service...
echo.

call venv\Scripts\activate.bat

echo Backend running on http://localhost:5000
echo Press Ctrl+C to stop
echo.

python run.py

pause
