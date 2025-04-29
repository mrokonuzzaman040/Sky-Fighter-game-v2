import socket
import json
import threading
import time
import queue

class GameClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.port = 5555
        self.socket = None
        self.connected = False
        self.player_id = None
        self.remote_position = (0, 0)
        self.remote_bullets = queue.Queue()
        self.receive_thread = None
        self.running = False
    
    def connect(self):
        """Connect to the game server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_address, self.port))
            
            # Get our player ID
            data = self.socket.recv(1024)
            response = json.loads(data.decode('utf-8'))
            self.player_id = response.get('player_id')
            
            # Start receive thread
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            print(f"Connected to server as Player {self.player_id + 1}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        self.running = False
        if self.socket:
            try:
                self.send_message({'type': 'disconnect'})
                self.socket.close()
            except:
                pass
            self.socket = None
        self.connected = False
    
    def get_player_id(self):
        """Get the player ID assigned by the server"""
        return self.player_id
    
    def send_message(self, message_dict):
        """Send a message to the server"""
        if not self.connected or not self.socket:
            return False
        
        try:
            message = json.dumps(message_dict)
            self.socket.send(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
            return False
    
    def send_position(self, x, y):
        """Send player position to server"""
        return self.send_message({
            'type': 'position',
            'x': x,
            'y': y
        })
    
    def send_bullet(self):
        """Send bullet fired event"""
        return self.send_message({
            'type': 'bullet',
            'x': -1,  # Server will use current player position
            'y': -1
        })
    
    def send_game_over(self):
        """Send game over notification"""
        return self.send_message({
            'type': 'game_over'
        })
    
    def get_remote_position(self):
        """Get the position of the remote player"""
        return self.remote_position
    
    def get_remote_bullets(self):
        """Get any remote bullets that have been fired"""
        bullets = []
        while not self.remote_bullets.empty():
            bullets.append(self.remote_bullets.get())
        return bullets
    
    def _receive_loop(self):
        """Internal method to continuously receive data from server"""
        while self.running and self.connected:
            try:
                data = self.socket.recv(1024)
                if data:
                    self._handle_message(data)
                else:
                    # Empty data means disconnected
                    self.connected = False
                    break
            except Exception as e:
                print(f"Receive error: {e}")
                self.connected = False
                break
        
        print("Receive thread ended")
    
    def _handle_message(self, data):
        """Process received message"""
        try:
            message = json.loads(data.decode('utf-8'))
            msg_type = message.get('type')
            
            if msg_type == 'position':
                self.remote_position = (message.get('x'), message.get('y'))
            
            elif msg_type == 'bullet':
                self.remote_bullets.put((message.get('x'), message.get('y')))
            
            elif msg_type == 'game_over':
                # Handle remote player game over
                pass
                
        except Exception as e:
            print(f"Message handling error: {e}")
