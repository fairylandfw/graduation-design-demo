@echo off
title Frontend Service
cd /d "%~dp0"

echo Starting Frontend Service...
echo.

if not exist node_modules (
    echo Installing dependencies...
    call npm install --registry=https://registry.npmmirror.com
)

echo Frontend will be available at http://localhost:8080
echo Press Ctrl+C to stop
echo.

npm run serve

pause
