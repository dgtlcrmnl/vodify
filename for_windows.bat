@echo off
REM Get the directory where this batch file lives
set "batch_dir=%~dp0"

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Download Python from https://www.python.org/
    pause
    exit /b
)

REM Create VOD directory
if not exist "%batch_dir%\Downloaded VODs" mkdir "%batch_dir%\Downloaded VODs"

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install streamlink ffmpeg-python

REM Run script
cd /d "%batch_dir%"
if exist "vodify.py" (
    python vodify.py
) else (
    echo Error: Missing vodify.py
    pause
)