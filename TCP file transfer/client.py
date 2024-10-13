#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: A program using TCP socket for wired network for file transfer (CLIENT MODULE)
# 
# Socket programming is a way of connecting two nodes on a network to communicate with each other.
# One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to
# form a connection. The server forms the listener socket while the client reaches out to the server.

import socket
import os
from config import *

def send_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
        
        # Send filename to server
        client.send(filename.encode())
        
        # Wait for server acknowledgment
        response = client.recv(1024).decode()
        print(f"Server response: {response}")
        
        # Send file data
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client.send(data)
            
            # Send EOF marker
            client.send(b'EOF')
        
        # Get final response from server
        final_response = client.recv(1024).decode()
        print(f"Server: {final_response}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        client.close()

if __name__ == "__main__":
    filename = input("Enter the filename to send: ")
    send_file(filename)