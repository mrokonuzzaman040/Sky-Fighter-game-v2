import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, master, start_game_callback, start_multiplayer_callback):
        self.master = master
        self.start_game_callback = start_game_callback
        self.start_multiplayer_callback = start_multiplayer_callback
        
        # Default settings
        self.screen_mode = "windowed"  # "windowed" or "fullscreen"
        self.screen_size = "800x600"   # Default size for windowed mode
        self.difficulty = "normal"
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", 
                        font=("Arial", 14, "bold"),
                        padding=10,
                        background="#4a7abc")
        
        # Create a frame with a background image
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Store reference to master for resize events
        self.master = master
        
        # Load background image
        self.load_background()
        
        # Bind resize event to update background
        master.bind('<Configure>', self.on_window_resize)
        
        # Game title
        self.title_label = tk.Label(self.frame, 
                                   text="SKY WARR",
                                   font=("Impact", 50, "bold"),
                                   fg="#ffd700",
                                   bg="#000000")
        self.title_label.pack(pady=(100, 50))
        
        # Create buttons
        self.btn_frame = tk.Frame(self.frame, bg="#333333")
        self.btn_frame.pack(pady=20)
        
        # Play button
        self.play_btn = ttk.Button(self.btn_frame, 
                                 text="Single Player",
                                 command=self.start_single_player,
                                 style="TButton")
        self.play_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Multiplayer Host button
        self.host_btn = ttk.Button(self.btn_frame, 
                                 text="Host Multiplayer",
                                 command=self.host_multiplayer,
                                 style="TButton")
        self.host_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Multiplayer Join button
        self.join_btn = ttk.Button(self.btn_frame, 
                                 text="Join Multiplayer",
                                 command=self.join_multiplayer,
                                 style="TButton")
        self.join_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Settings button
        self.settings_btn = ttk.Button(self.btn_frame, 
                                     text="Settings",
                                     command=self.open_settings,
                                     style="TButton")
        self.settings_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Exit button
        self.exit_btn = ttk.Button(self.btn_frame, 
                                 text="Exit",
                                 command=self.master.quit,
                                 style="TButton")
        self.exit_btn.pack(pady=10, padx=20, fill=tk.X)
    
    def start_single_player(self):
        """Start single player game with current settings"""
        self.start_game_callback(self.difficulty, self.screen_mode, self.screen_size)
    
    def host_multiplayer(self):
        """Host a multiplayer game"""
        # Start a multiplayer game as host
        self.start_multiplayer_callback("localhost", True, self.screen_mode, self.screen_size)
    
    def join_multiplayer(self):
        """Open dialog to join a multiplayer game"""
        join_window = tk.Toplevel(self.master)
        join_window.title("Join Multiplayer Game")
        join_window.geometry("400x200")
        join_window.transient(self.master)
        join_window.grab_set()
        
        # Add server IP input
        ip_frame = ttk.Frame(join_window)
        ip_frame.pack(padx=20, pady=20, fill=tk.X)
        
        ttk.Label(ip_frame, text="Server IP:").pack(side=tk.LEFT)
        ip_var = tk.StringVar(value="localhost")
        ip_entry = ttk.Entry(ip_frame, textvariable=ip_var, width=20)
        ip_entry.pack(side=tk.LEFT, padx=10)
        
        # Connect button
        def connect():
            server_ip = ip_var.get()
            join_window.destroy()
            self.start_multiplayer_callback(server_ip, False, self.screen_mode, self.screen_size)
            
        ttk.Button(join_window, text="Connect", 
                 command=connect).pack(pady=20)
        
        # Cancel button
        ttk.Button(join_window, text="Cancel", 
                 command=join_window.destroy).pack(pady=5)
    
    def open_settings(self):
        """Open the settings dialog"""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.master)
        settings_window.grab_set()
        
        # Difficulty settings
        difficulty_frame = ttk.LabelFrame(settings_window, text="Difficulty")
        difficulty_frame.pack(padx=20, pady=10, fill=tk.X)
        
        difficulty_var = tk.StringVar(value=self.difficulty)
        
        ttk.Radiobutton(difficulty_frame, text="Easy", 
                      variable=difficulty_var, value="easy").pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Normal", 
                      variable=difficulty_var, value="normal").pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Hard", 
                      variable=difficulty_var, value="hard").pack(anchor=tk.W)
        
        # Screen mode settings
        screen_frame = ttk.LabelFrame(settings_window, text="Screen Mode")
        screen_frame.pack(padx=20, pady=10, fill=tk.X)
        
        screen_mode_var = tk.StringVar(value=self.screen_mode)
        
        ttk.Radiobutton(screen_frame, text="Windowed", 
                      variable=screen_mode_var, value="windowed").pack(anchor=tk.W)
        ttk.Radiobutton(screen_frame, text="Fullscreen", 
                      variable=screen_mode_var, value="fullscreen").pack(anchor=tk.W)
        
        # Screen size settings (for windowed mode)
        size_frame = ttk.LabelFrame(settings_window, text="Window Size (Windowed Mode)")
        size_frame.pack(padx=20, pady=10, fill=tk.X)
        
        screen_size_var = tk.StringVar(value=self.screen_size)
        
        sizes = ["800x600", "1024x768", "1280x720", "1366x768", "1600x900", "1920x1080"]
        for size in sizes:
            ttk.Radiobutton(size_frame, text=size, 
                          variable=screen_size_var, value=size).pack(anchor=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(pady=20)
        
        # Save button
        def save_settings():
            self.difficulty = difficulty_var.get()
            self.screen_mode = screen_mode_var.get()
            self.screen_size = screen_size_var.get()
            settings_window.destroy()
            
        ttk.Button(button_frame, text="Save", 
                 command=save_settings).pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", 
                 command=settings_window.destroy).pack(side=tk.LEFT, padx=5)

    def load_background(self):
        """Load and resize background image to current window size"""
        try:
            # Create directories if they don't exist
            os.makedirs("assets/images", exist_ok=True)
            
            # Get current window size
            self.master.update_idletasks()  # Ensure geometry is updated
            width = self.master.winfo_width()
            height = self.master.winfo_height()
            
            # Load and resize background image
            self.bg_image = Image.open("assets/images/menu_bg.jpg")
            self.bg_image = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            
            # Create or update background label
            if hasattr(self, 'bg_label'):
                self.bg_label.configure(image=self.bg_photo)
            else:
                self.bg_label = tk.Label(self.frame, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.frame.configure(bg="#2c3e50")
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        # Only resize background for the main window, not child dialogs
        if event.widget == self.master:
            # Delay the background reload slightly to avoid too many calls
            self.master.after(100, self.load_background)
