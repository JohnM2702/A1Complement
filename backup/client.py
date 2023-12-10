import socket
import pickle
import threading
from observer import Observable, Observer

player_size_data = 0

server_message_received = threading.Event()

class Client(Observable):
    
    def __init__(self, ip = None, port = 5566, size = 4096, name = "Juan") -> None:
        self.ip = self.get_ip()
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = size
        self.format = "utf-8"
        
        self.client = None
        
        self.name = name
    
    def start(self):
        # Client initialization
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.addr = (self.ip, self.port)
        self.client.connect(self.addr)
        print(f"[THIS CLIENT] Connected to server at {self.ip}:{self.port}")

        # Handle server incoming msg
        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client,))
        receive_thread.start()
        
        # Send player information
        try:
            self.client.send((self.name+" - "+self.ip+":"+str(self.port)).encode(self.format))
        except Exception as e:
            print(f"[ERROR] {e}")
        

    def get_name(self):
        return self.name

    def send_message(self, message):
        try:
            if isinstance(message, str):
                data = message.encode(self.format)
            else:
                data = pickle.dumps(message)
            self.client.send(data)
        except Exception as e:
            print(f"[ERROR] {e}")
          
    def receive_messages(self, client_socket):
        global player_size_data
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
            
            print("\nServer broadcast: "+f"{recv_data}"+"\n")
            self.notify(recv_data)
            
            if recv_data[0].isdigit():
                player_size_data = recv_data.split(",")
           
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


client_ref = None

def get_client_name():
    global client_ref
    return client_ref.get_name()

def get_server_size():
    global player_size_data
    return player_size_data

def client_message(message):
    global client_ref
    client_ref.send_message(message)

def client_init(server_ip="192.168.1.1", player_name="Juan"):
    global client_ref
    client_obj = Client(ip=server_ip, name=player_name)
    client_ref = client_obj

def client_start():
    global client_ref
    client_ref.start()

    # start() should be seperated
    