#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: Wordle game to learn socket programming (SERVER MODUILE)
# 
# Socket programming is a way of connecting two nodes on a network to communicate with each other.
# One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to
# form a connection. The server forms the listener socket while the client reaches out to the server.
# 
#  Wordle game: 
#  Players have six attempts to guess a five-letter word
#  you will recieve feedback for each guess in the form of aestricks and correct word placements indicating when letters match or occupy the correct position

import socket
import threading
import random
from config import *

class WordleGame:
    def __init__(self):
        self.target_word = random.choice(word_list)
        self.active_connections = 0
        self.connection_lock = threading.Lock()
        self.active_players = {}  # Dictionary to store player names
        
    def validate_guess(self, guess):
        if len(guess) != WORD_LENGTH:
            return "Invalid word length"
            
        result = ['*'] * WORD_LENGTH
        for i in range(WORD_LENGTH):
            if guess[i] == self.target_word[i]:
                result[i] = guess[i]
                
        correct_chars = sum(1 for i in range(WORD_LENGTH) if guess[i] == self.target_word[i])
        return f"{''.join(result)} (Correct characters: {correct_chars})"

    def add_player(self, player_name):
        with self.connection_lock:
            if self.active_connections >= MAX_PLAYERS:
                return False
            self.active_connections += 1
            player_number = self.active_connections
            self.active_players[player_number] = player_name
            return player_number
            
    def remove_player(self, player_number):
        with self.connection_lock:
            if self.active_connections > 0:
                self.active_connections -= 1
                if player_number in self.active_players:
                    del self.active_players[player_number]

def handle_client(client_socket, addr, game):
    try:
        player_name = client_socket.recv(1024).decode().strip()
        player_number = game.add_player(player_name)
        if not player_number:
            client_socket.send("Room is full. Please try again later.".encode())
            client_socket.close()
            return
        
        print(f"Player {player_number} ({player_name}) connected from {addr}")
        client_socket.send(f"Welcome {player_name}! You have {MAX_ATTEMPTS} attempts.".encode())
        
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                guess = client_socket.recv(1024).decode().strip().lower()
                if not guess:  # Client disconnected
                    break
                    
                attempts += 1
                print(f"Player {player_number} ({player_name}) - Attempt {attempts}/{MAX_ATTEMPTS}: {guess}")
                
                result = game.validate_guess(guess)
                client_socket.send(result.encode())
                
                if guess == game.target_word:
                    client_socket.send(f"\nCongratulations {player_name}! You won in {attempts} attempts!".encode())
                    break
                    
                if attempts == MAX_ATTEMPTS:
                    client_socket.send(f"\nGame Over {player_name}! The word was: {game.target_word}".encode())
                    
            except ConnectionError:
                break
                
    finally:
        print(f"Player {player_number} ({player_name}) disconnected")
        game.remove_player(player_number)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")
    
    game = WordleGame()
    
    while True:
        try:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, 
                                   args=(client_socket, addr, game))
            thread.daemon = True
            thread.start()
            
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
            
    server_socket.close()

if __name__ == "__main__":
    start_server()