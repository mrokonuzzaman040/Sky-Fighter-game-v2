import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, master, start_game_callback, start_multiplayer_callback):
        self.master = master
        self.start_game_callback = start_game_callback
        self.start_multiplayer_callback = start_multiplayer_callback
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", 
                        font=("Arial", 14, "bold"),
                        padding=10,
                        background="#4a7abc")
        
        # Create a frame with a background image
        self.frame = tk.Frame(master, width=800, height=600)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Load background image
        try:
            # Create directories if they don't exist
            os.makedirs("assets/images", exist_ok=True)
            
            self.bg_image = Image.open("assets/images/menu_bg.jpg")
            self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.frame, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.frame.configure(bg="#2c3e50")
        
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
                                 command=self.start_game_callback,
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
    
    def host_multiplayer(self):
        """Host a multiplayer game"""
        # Start a multiplayer game as host
        self.start_multiplayer_callback("localhost", True)
    
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
            self.start_multiplayer_callback(server_ip, False)
            
        ttk.Button(join_window, text="Connect", 
                 command=connect).pack(pady=20)
        
        # Cancel button
        ttk.Button(join_window, text="Cancel", 
                 command=join_window.destroy).pack(pady=5)
    
    def open_settings(self):
        """Open the settings dialog"""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.master)
        settings_window.grab_set()
        
        # Add settings controls here
        difficulty_frame = ttk.LabelFrame(settings_window, text="Difficulty")
        difficulty_frame.pack(padx=20, pady=20, fill=tk.X)
        
        difficulty_var = tk.StringVar(value="normal")
        
        ttk.Radiobutton(difficulty_frame, text="Easy", 
                      variable=difficulty_var, value="easy").pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Normal", 
                      variable=difficulty_var, value="normal").pack(anchor=tk.W)
        ttk.Radiobutton(difficulty_frame, text="Hard", 
                      variable=difficulty_var, value="hard").pack(anchor=tk.W)
        
        # Save button
        ttk.Button(settings_window, text="Save", 
                 command=lambda: settings_window.destroy()).pack(pady=20)
