#!/bin/bash

# setup_and_run.sh

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Install it with: sudo apt install python3 (Debian/Ubuntu) or brew install python (macOS)"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install/upgrade Streamlink
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install streamlink

# Check for Python script
if [ -f "$SCRIPT_DIR/vodify.py" ]; then
    echo "Starting downloader..."
    cd "$SCRIPT_DIR" || exit
    python3 vodify.py
else
    echo "Error: vodify.py not found in:"
    echo "$SCRIPT_DIR"
    echo "Make sure:"
    echo "1. Both setup_and_run.sh and vodify.py are in the same directory"
    echo "2. Files haven't been renamed"
    exit 1
fi