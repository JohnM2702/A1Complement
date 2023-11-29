import os
import platform
import socket
import pickle
import threading
from time import sleep
from gamestate import GameState
import random

class Server:
    def __init__(self, port = 5566, size = 4096, max_connection = 1) -> None:
        self.ip = self.get_ip()
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = size
        self.format = "utf-8"
        self.server_id = (f"[Server {socket.gethostname()} ({self.ip}:{self.port})]")
        self.max_connection = max_connection
        
        self.clients = []
        self.clients_lock = threading.Lock()

    def start(self):
        print(f"{self.server_id} Server is starting...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(self.addr)
            server.listen(self.max_connection)
        except:
            print(f"{self.server_id} Server failed to start. Port {self.port} is currently in use by another process.")
            return
        print(f"{self.server_id} Server is listening on {self.ip}:{self.port}")

        while len(self.clients) < self.max_connection:
            conn, addr = server.accept()
            client_info = {"connection": conn, "address": addr}
            with self.clients_lock:
                self.clients.append(client_info)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()  

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                if isinstance(message, str):
                    data = message.encode(self.format)
                else:
                    data = pickle.dumps(message)
                client["connection"].sendall(data)
            except Exception as e:
                print(f"[ERROR] {e}")

    def handle_client(self, conn, addr):
        
        CLIENT_ID = (f"[Client ({addr[0]} @ {addr[1]})]")
        print(f"{CLIENT_ID}  Estabilished connection to server.")
        
        connected = True
        while connected:
            try:
                recv_data_binary = conn.recv(self.size)
            except ConnectionResetError:
                print(f"[{addr[0]}] Disconnected")
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
            
            print(f"[{addr[0]}] {recv_data}")
            self.broadcast_message(recv_data)

                
        with self.clients_lock:
            self.clients[:] = [client for client in self.clients if client["address"] != addr]

        try:
            conn.close()
        except Exception as e:
            print(f"[ERROR] {e}")       

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

class QuestionAnswerContainer:
    def __init__(self) -> None:
        self.qna_list = []

    def add_qna(self, new_qna:dict):
        """        
        {
            "q": "question/trivia",
            "a": "answer"
        }
        """
        self.qna_list.append(new_qna)

    def write_to_file(self):
        pickle_file = open('pickled_qna', 'ab')
        
        pickle.dump(self.qna_list, pickle_file)   

        pickle_file.close()

    def read_from_file(self):
        pickle_file = open('pickled_qna', 'rb')    

        extracted_qna_list = pickle.load(pickle_file)
        self.qna_list = extracted_qna_list

        pickle_file.close()

    def qna_list_dump(self):
        #- prints all qna and its corresponding index
        for index in range(len(self.qna_list)):
            print(f"{index}")
            print("q: " + str(self.qna_list[index]["q"]))
            print("a: " + str(self.qna_list[index]["a"]))
            print()
            
    def get_random_qna(self, number=1):
        if number > len(self.qna_list):
            print("Warning: The requested number is greater than the number of available Q&A pairs.")
            random.shuffle(self.qna_list)
            return self.qna_list

        random_qna_list = random.sample(self.qna_list, number)
        return random_qna_list

            
def main(max_players=4):
    server_obj = Server(max_connection=max_players)
    qna_obj = QuestionAnswerContainer()
    qna_obj.read_from_file()
    server_obj.start()
    
    
    
    
    
import sys


if __name__ == "__main__":
    main(max_players=sys.argv[1])