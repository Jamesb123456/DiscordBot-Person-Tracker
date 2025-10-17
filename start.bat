@echo off
echo Starting FiveM Player Tracker Bot...
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import discord" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    echo.
)

echo Starting bot...
echo.
python bot.py

pause
