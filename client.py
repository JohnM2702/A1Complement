import random
import socket
import pickle
import threading
from time import sleep
from gamestate import GameState
import time

class Server:
    def __init__(self, ip = None, port = 5566, size = 4096, max_connection = 5) -> None:
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = size
        self.format = "utf-8"
        self.client_id = (f"[Server {socket.gethostname()} ({self.ip}:{self.port})]")
        
        self.client = None

    def receive_messages(self, client_socket):
        while True:
            try:
                recv_data_binary = client_socket.recv(self.size)
            except ConnectionAbortedError:
                print(f"Disconnected from server")
                break
            except ConnectionResetError:
                print(f"[ERROR] Server closed unexpectedly. Check server status.")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break
                
            try:
                recv_data = recv_data_binary.decode()
            except UnicodeDecodeError:
                recv_data = pickle.loads(recv_data_binary)
            except Exception as e:
                print(f"[ERROR] {e}")
                break
            
            print(f"{recv_data}")
            
    
    def start(self, pname = None):
        pname = "PNAME:" + str(input("Player Name: "))
        
        # Client initialization
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)
        print(f"[THIS CLIENT] Connected to server at {self.ip}:{self.port}")

        # Handle server incoming msg
        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client,))
        receive_thread.start()
        
        # Send player information
        try:
            self.client.send(pname.encode(self.format))
        except Exception as e:
            print(f"[ERROR] {e}")
                
            
    def send_message(self, message):
        try:
            if isinstance(message, str):
                data = message.encode(self.format)
            else:
                data = pickle.dumps(message)
            self.client.send(data)
        except Exception as e:
            print(f"[ERROR] {e}")
        


    # client.close()

x = Server(ip=str(input("IP:")))
x.start()
input("Enter to start")
while True:
    x.send_message(input("> "))