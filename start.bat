@echo off
title Sentiment Analysis Platform
color 0A
echo.
echo ========================================
echo   Sentiment Analysis Platform
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Installing backend dependencies...
cd backend

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [2/4] Initializing database...
python init_db.py

echo.
echo [3/4] Collecting latest data...
python auto_crawler.py

echo.
echo [4/4] Starting services...
start "Backend" cmd /k "title Backend Service && cd /d %~dp0backend && call venv\Scripts\activate.bat && python run.py"

timeout /t 3 /nobreak >nul

cd ..\frontend
start "Frontend" cmd /k "title Frontend Service && cd /d %~dp0frontend && npm run serve"

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:8080

echo.
echo Close the Backend and Frontend windows to stop.
pause
