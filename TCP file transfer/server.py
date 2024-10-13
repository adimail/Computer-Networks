#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: A program using TCP socket for wired network for file transfer (SERVER MODULE)
# 
# Socket programming is a way of connecting two nodes on a network to communicate with each other.
# One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to
# form a connection. The server forms the listener socket while the client reaches out to the server.

import socket
from config import *

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((HOST, PORT))
    
    # Listen for incoming connections
    server.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address} has been established!")
        
        try:
            # Receive the filename from client
            filename = client_socket.recv(1024).decode()
            print(f"Client wants to send file: {filename}")
            
            # Send acknowledgment
            client_socket.send("Ready to receive".encode())
            
            # Open a new file to write the incoming data
            with open(f"received_{filename}", 'wb') as file:
                while True:
                    # Receive data from client
                    data = client_socket.recv(1024)
                    if not data or data == b'EOF':
                        break
                    # Write data to file
                    file.write(data)
            
            print(f"File '{filename}' received successfully")
            client_socket.send("File received successfully".encode())
            
        except Exception as e:
            print(f"Error: {e}")
            client_socket.send("Error occurred during transfer".encode())
            
        finally:
            client_socket.close()
            
if __name__ == "__main__":
    start_server()