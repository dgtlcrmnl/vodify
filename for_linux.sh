#!/bin/bash

# Create VOD directory
mkdir -p "Downloaded VODs"

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "Python 3 required: https://www.python.org/"
    exit 1
fi

# Install requirements
python3 -m pip install --upgrade pip
python3 -m pip install streamlink ffmpeg-python

# Run script
if [ -f "vodify.py" ]; then
    python3 vodify.py
else
    echo "Error: Missing vodify.py"
    exit 1
fi