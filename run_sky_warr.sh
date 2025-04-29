#!/bin/bash

# Sky Warr Game Setup and Run Script
# This script will set up a virtual environment, install dependencies,
# create necessary assets, and run the Sky Warr game.

echo "===== Sky Warr Game Setup and Run Script ====="
echo "Setting up environment for Sky Warr game..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please make sure you have the venv module installed."
        echo "You can install it with: sudo apt-get install python3-venv (for Debian/Ubuntu)"
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install or upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Clean up the requirements file by removing tkinter (it's a system package)
echo "Fixing requirements file..."
TEMP_REQUIREMENTS=$(mktemp)
grep -v "^tkinter$" requirements.txt > "$TEMP_REQUIREMENTS"

# Install required packages
echo "Installing required packages..."
pip install -r "$TEMP_REQUIREMENTS"
rm "$TEMP_REQUIREMENTS"

# Make sure tkinter is installed (system package)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Warning: tkinter is not installed, which is required for the game menu."
    echo "On Debian/Ubuntu, install it with: sudo apt-get install python3-tk"
    echo "On Fedora: sudo dnf install python3-tkinter"
    echo "On macOS: brew install python-tk"
    
    read -p "Would you like to attempt installing tkinter automatically? (y/n) " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        if command -v apt-get &> /dev/null; then
            echo "Detected Debian/Ubuntu. Installing python3-tk..."
            sudo apt-get install -y python3-tk
        elif command -v dnf &> /dev/null; then
            echo "Detected Fedora. Installing python3-tkinter..."
            sudo dnf install -y python3-tkinter
        elif command -v brew &> /dev/null; then
            echo "Detected macOS with Homebrew. Installing python-tk..."
            brew install python-tk
        else
            echo "Couldn't detect package manager. Please install tkinter manually."
        fi
    fi
fi

# Install missing Python packages explicitly
echo "Installing critical packages..."
pip install pillow pygame python-dotenv flask flask-socketio

# Create game assets if needed
echo "Creating game assets if needed..."
python3 create_assets.py

# Run the game
echo "Starting Sky Warr game..."
python3 main.py

# Deactivate virtual environment
deactivate

echo "Game closed. Thanks for playing Sky Warr!"