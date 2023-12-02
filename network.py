import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.13"
        self.port = 5566
        self.addr = (self.server, self.port)
        self.ip = self.get_ip()
        self.client.connect(self.addr)
    
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
        try: 
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def send(self, data):
        try:
            self.client.sendall(str.encode(data))
            return self.receive_pickle()
        except socket.error as e:
            print(e)
    
    def send_create(self, player_size, name):
        data = f'create,{player_size},{self.ip},{name}'
        return self.send(data)

    def send_join(self, game_id, name):
        data = f'join,{game_id},{self.ip},{name}'
        return self.send(data)

    def wait_for_players(self):
        try:
            self.client.sendall(str.encode('waiting'))
            return self.receive_pickle()
        except socket.error as e:
            print(e)
    
    def receive_pickle(self):
        # Buffer to store received data
        buffer_size = 1024
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
