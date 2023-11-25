import random
import socket
import pickle
import threading
from time import sleep
from gamestate import GameState
import time

# Client Configurations
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
index = -1

def receive_messages(client_socket):
    while True:
        try:
            header = client_socket.recv(len(b'SERIALIZED:'))
            if header == b'SERIALIZED:':
                data = client_socket.recv(SIZE)
                temp = pickle.loads(data)
                print(temp)
            else:
                print(f"[SERVER] {header.decode(FORMAT)}")
            
            if 'GSET:' in header.decode(FORMAT):
                index = header.decode(FORMAT).replace('GSET:','')
                
                
        except ConnectionAbortedError:
            print(f"Disconnected from server")
            connected = False
            break
        except ConnectionResetError:
            print(f"[ERROR] Server closed unexpectedly. Check server status.")
            connected = False
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False
            break


def game_proper(index):
    word_lists = [
        ["apple", "banana", "orange"],
        ["car", "bike", "bus"],
        ["cat", "dog", "bird"]
    ]
    
    current_word_list = word_lists[index]
    
    start_time = time.time()

    while time.time() - start_time < 60:
        current_word = random.choice(current_word_list)
        user_guess = input(f"Guess the word: {', '.join(current_word_list)}? ").lower()

        if user_guess == current_word:
            print("Congratulations! You guessed the word correctly.")
            break
        else:
            print("Incorrect. Try again!")

    print("Time's up! Thanks for playing.")

connected = True
def main():
    pname = "PNAME:" + str(input("Player Name: "))
    
    # Client initialization
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[THIS CLIENT] Connected to server at {IP}:{PORT}")

    # Handle server incoming msg
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    
    # Send player information
    try:
        client.send(pname.encode(FORMAT))
    except Exception as e:
        print(f"[ERROR] {e}")
            
            
    sleep(5)
    game_proper(index)

    
    
    client.close()


if __name__ == "__main__":
    main()