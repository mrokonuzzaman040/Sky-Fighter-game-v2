import socket
import json
import threading
import time

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = [None, None]  # Max 2 players
        self.client_addresses = ['', '']
        self.running = False
    
    def start(self):
        """Start the game server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)  # Max 2 connections
            
            self.running = True
            print(f"Server started on {self.host}:{self.port}")
            
            # Accept connections
            while self.running:
                client_socket, address = self.server_socket.accept()
                self._handle_new_connection(client_socket, address)
                
        except Exception as e:
            print(f"Server error: {e}")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop the game server"""
        self.running = False
        
        # Close all client connections
        for i, client in enumerate(self.clients):
            if client:
                try:
                    client.close()
                except:
                    pass
                self.clients[i] = None
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
            
        print("Server stopped")
    
    def _handle_new_connection(self, client_socket, address):
        """Process a new client connection"""
        # Find an empty slot
        player_id = -1
        for i in range(len(self.clients)):
            if self.clients[i] is None:
                player_id = i
                self.clients[i] = client_socket
                self.client_addresses[i] = address
                break
        
        if player_id == -1:
            # No slots available
            try:
                client_socket.send(json.dumps({'error': 'Server full'}).encode('utf-8'))
                client_socket.close()
            except:
                pass
            return
        
        print(f"Player {player_id + 1} connected from {address}")
        
        # Send player ID to client
        try:
            client_socket.send(json.dumps({'player_id': player_id}).encode('utf-8'))
        except:
            self.clients[player_id] = None
            return
        
        # Start a thread to handle this client
        client_thread = threading.Thread(
            target=self._handle_client, 
            args=(client_socket, player_id)
        )
        client_thread.daemon = True
        client_thread.start()
    
    def _handle_client(self, client_socket, player_id):
        """Handle communication with a connected client"""
        while self.running:
            try:
                # Receive data
                data = client_socket.recv(1024)
                if not data:
                    break  # Connection closed
                
                # Process message
                self._process_message(data, player_id)
                
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                break
        
        # Clean up when client disconnects
        print(f"Player {player_id + 1} disconnected")
        try:
            client_socket.close()
        except:
            pass
        self.clients[player_id] = None
    
    def _process_message(self, data, sender_id):
        """Process a message from a client and forward to the other client"""
        try:
            message = json.loads(data.decode('utf-8'))
            msg_type = message.get('type')
            
            # Forward to the other player
            other_id = 1 - sender_id  # Toggle between 0 and 1
            if self.clients[other_id]:
                try:
                    self.clients[other_id].send(data)
                except:
                    pass
            
            # Handle disconnect specially
            if msg_type == 'disconnect':
                raise Exception("Client disconnected")
                
        except Exception as e:
            print(f"Message processing error: {e}")

def start_server():
    """Start the game server"""
    server = GameServer()
    server.start()

def start_server_thread():
    """Start the server in a separate thread"""
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(0.5)
    return server_thread

# If this script is run directly, start the server
if __name__ == "__main__":
    print("Starting Sky Warr multiplayer server...")
    start_server()
