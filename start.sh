#!/bin/bash
echo "=== SkyCore Supreme ==="
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 start.py
