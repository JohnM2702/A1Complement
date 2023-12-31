import dill as pickle
import socket
import re

class Network:
    def __init__(self, server_ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = 5566
        self.addr = (self.server, self.port)
        self.ip = self.get_ip()
    
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
    
    def connect(self):
        if self.is_valid_ip(self.server):    
            try:
                self.client.settimeout(1)
                self.client.connect(self.addr)
                self.client.settimeout(None)
                return True
            except Exception as e:
                print(f'Failed to connect to the server: {e}')
                return False
        else:
            return False
    
    def send_and_receive(self, data):
        try:
            if not isinstance(data, str):
                data = str(data)
            self.client.sendall(data.encode('utf-8'))
            return self.receive_pickle()
        except socket.error as e:
            print(e)
            
    def send(self, data):
        try:
            if not isinstance(data, str):
                data = str(data)
            self.client.sendall(data.encode('utf-8'))
        except socket.error as e:
            print(e)

    def receive_game_data(self):
        try:
            self.client.sendall(str.encode(' '))
            return self.receive_pickle()
        except socket.error as e:
            print(e)
    
    def receive_pickle(self):
        # Buffer to store received data
        buffer_size = 4096
        data_buffer = b""

        while True:
            data_chunk = self.client.recv(buffer_size)
            if not data_chunk:
                break

            data_buffer += data_chunk

            try:
                # Attempt to unpickle the received data
                unpickled_object = pickle.loads(data_buffer)
                return unpickled_object
            except pickle.UnpicklingError:
                # Continue receiving data until a complete pickled object is obtained
                continue

    def is_valid_ip(self, input_str):
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if ip_pattern.match(input_str):
            segments = list(map(int, input_str.split('.')))
            if all(0 <= segment <= 255 for segment in segments):
                return True
        return False
