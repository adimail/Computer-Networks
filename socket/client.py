#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: Wordle game to learn socket programming (CLIENT MODUILE)
# 
# Socket programming is a way of connecting two nodes on a network to communicate with each other.
# One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to
# form a connection. The server forms the listener socket while the client reaches out to the server.
# 
#  Wordle game: 
#  Players have six attempts to guess a five-letter word
#  you will recieve feedback for each guess in the form of aestricks and correct word placements indicating when letters match or occupy the correct position

import socket
from config import port

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        player_name = input("Enter your name: ")
        client_socket.connect(('localhost', port))
        client_socket.send(player_name.encode())
        welcome_msg = client_socket.recv(1024).decode()
        print(welcome_msg)
        
        # Check if room is full
        if "Room is full" in welcome_msg:
            return
        
        while True:
            guess = input("Enter your guess (5 letters): ")
            client_socket.send(guess.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")
            
            if "Congratulations" in response or "Game Over" in response:
                play_again = input("\nWould you like to play again? (yes/no): ")
                if play_again.lower() != 'yes':
                    break
                else:
                    print("Starting new game...")
                    return start_client()
                
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()