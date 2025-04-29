# Sky Warr

A space shooter game with both single-player and multiplayer modes.

## Quick Start

The easiest way to get started is by using our setup script:

```bash
# Clone the repository
git clone https://github.com/mrokonuzzaman040/Sky-Fighter-game-v2.git
cd Sky-Fighter-game-v2

# Make the script executable (if needed)
chmod +x run_sky_warr.sh

# Run the setup script
./run_sky_warr.sh
```

This script will:
1. Set up a Python virtual environment
2. Install all required dependencies
3. Create necessary game assets
4. Launch the game automatically

## Prerequisites

- Python 3.7 or higher
- tkinter (for the game menu)
- Git (for cloning the repository)

## Installation Options

### Option 1: Using the Setup Script (Recommended)

The `run_sky_warr.sh` script handles everything automatically:

```bash
# Clone the repository
git clone https://github.com/mrokonuzzaman040/Sky-Fighter-game-v2.git
cd Sky-Fighter-game-v2

# Run the setup script
./run_sky_warr.sh
```

If you're on Windows using Git Bash or WSL, the script should work as well.

### Option 2: Install with pip

```bash
# Clone the repository
git clone https://github.com/mrokonuzzaman040/Sky-Fighter-game-v2.git
cd Sky-Fighter-game-v2

# Install the package
pip install .
```

### Option 3: Build standalone executable

First, make sure you have PyInstaller installed:

```bash
pip install pyinstaller
```

Then run the build script:

```bash
python build.py
```

This will:

1. Create game assets if they don't exist
2. Build a standalone executable package in the `dist/SkyWarr` directory
3. Create an installer appropriate for your platform (Windows .exe or Linux .deb)

#### Linux Requirements for Creating .deb Package

On Linux, to create a .deb package, you need the `dpkg-dev` package:

```bash
sudo apt-get install dpkg-dev
```

#### Windows Requirements for Creating Installer

On Windows, to create an installer, you need NSIS (Nullsoft Scriptable Install System):

1. Download and install from: https://nsis.sourceforge.io/Download
2. Make sure it's installed in the default location (C:/Program Files/NSIS or C:/Program Files (x86)/NSIS)

## Running the Game

### If using the setup script:

Just run:
```bash
./run_sky_warr.sh
```

### If installed via pip:

```bash
skywarr
```

### If using the standalone executable:

- On Windows: Run `SkyWarr.exe` from the installation directory
- On Linux: Run `skywarr` from the terminal

## Game Controls

- Arrow keys or A/D: Move the spaceship left and right
- Space: Fire
- Escape: Exit the game
- R: Restart (single-player mode only, after game over)

## Multiplayer Mode

The game supports two players playing over a network:

1. One player hosts the game (selects "Host Multiplayer")
2. The other player joins (selects "Join Multiplayer" and enters the host's IP address)

Both players must be able to establish a connection on port 5555.

## Troubleshooting

If you encounter issues with the setup script:

1. **Missing tkinter**: Some Linux distributions don't include tkinter by default
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install python3-tk
   ```

2. **Installation fails**: Make sure you have the latest pip
   ```bash
   pip install --upgrade pip
   ```

3. **Game assets not appearing**: Try running create_assets.py manually
   ```bash
   python create_assets.py
   ```
