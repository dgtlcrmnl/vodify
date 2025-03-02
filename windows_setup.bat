@echo off
REM Get the directory where this batch file lives
set "batch_dir=%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Download Python from https://www.python.org/ and ensure "Add Python to PATH" is checked
    pause
    exit /b
)

REM Install Streamlink
python -m pip install --upgrade pip
python -m pip install streamlink

REM Navigate to batch file's directory
cd /d "%batch_dir%"

REM Run the Python script with explicit path checking
if exist "vodify.py" (
    python vodify.py
) else (
    echo Error: File 'vodify.py' not found in:
    echo %batch_dir%
    echo Make sure:
    echo 1. You renamed the Python file to vodify.py
    echo 2. Both files are in the same folder
    echo 3. File extensions aren't hidden (shouldn't be .py.txt)
    pause
)