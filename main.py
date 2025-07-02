import os
import sys
import tkinter as tk
import pygame

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.menu import MainMenu
from game.game import Game
from network.client import GameClient

# Create required directories
def create_asset_directories():
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)

class SkyWarr:
    def __init__(self):
        # Create directories
        create_asset_directories()
        
        # Initialize Tkinter root
        self.root = tk.Tk()
        self.root.title("Sky Warr")
        self.root.geometry("800x600")
        self.root.resizable(True, True)  # Allow window resizing and maximizing
        
        # Set minimum window size to maintain usability
        self.root.minsize(600, 480)
        
        # Set icon if available
        try:
            self.root.iconphoto(True, tk.PhotoImage(file="assets/images/icon.png"))
        except:
            pass
        
        # Initialize main menu
        self.main_menu = MainMenu(self.root, self.start_game, self.start_multiplayer)
        
        # Initialize pygame
        pygame.init()
        
        # Game instance (will be created when game starts)
        self.game = None
        self.client = None
    
    def start_game(self, difficulty="normal", screen_mode="windowed", screen_size="800x600"):
        """Start the single-player game with the selected difficulty and screen settings"""
        # Hide Tkinter window
        self.root.withdraw()
        
        # Start the game
        self.game = Game(difficulty, screen_mode=screen_mode, screen_size=screen_size)
        self.game.run()
        
        # When game ends, show Tkinter window again
        self.root.deiconify()
    
    def start_multiplayer(self, server_address, is_host=False, screen_mode="windowed", screen_size="800x600"):
        """Start a multiplayer game"""
        # Hide Tkinter window
        self.root.withdraw()
        
        # Create network client
        self.client = GameClient(server_address)
        
        if is_host and server_address == "localhost":
            # Import here to avoid circular import
            from network.server import start_server_thread
            # Start server thread if we're hosting
            start_server_thread()
        
        # Try to connect
        if self.client.connect():
            # Start the game in multiplayer mode
            self.game = Game("normal", multiplayer=True, client=self.client, 
                           screen_mode=screen_mode, screen_size=screen_size)
            self.game.run()
        else:
            # Connection failed
            print("Failed to connect to server")
        
        # When game ends, show Tkinter window again
        self.root.deiconify()
    
    def run(self):
        """Run the main application loop"""
        self.root.mainloop()

def main():
    """Entry point function for pip installation"""
    app = SkyWarr()
    app.run()

if __name__ == "__main__":
    app = SkyWarr()
    app.run()
