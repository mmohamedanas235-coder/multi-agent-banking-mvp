@echo off
title NEXUS Core Banking AI — Multi-Agent Operational System
echo ===============================================================================
echo            NEXUS CORE BANKING AI — AUTONOMOUS MULTI-AGENT SYSTEM
echo ===============================================================================
echo.
echo [1/3] Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/3] Installing dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo [3/3] Launching NEXUS Banking AI Application Server...
echo.
echo Access the application at:
echo   --> Local UI: http://127.0.0.1:8000
echo   --> API Docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to terminate the server.
echo ===============================================================================
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
