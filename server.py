import socket
import pickle
import threading
import random
from observer import Observable, Observer

server_ref = None
qna_ref = None

class Server(Observable):
    def __init__(self, port = 5566, size = 4096, max_connection = 4) -> None:
        super(Server, self).__init__()
        self.ip = self.get_ip()
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = size
        self.format = "utf-8"
        self.max_connection = max_connection
        
        self.clients = []
        self.clients_lock = threading.Lock()

    def send_to_client(self, conn, message):
        try:
            if isinstance(message, str):
                data = message.encode(self.format)
            else:
                data = pickle.dumps(message)
            conn.sendall(data)
        except Exception as e:
            print(f"[ERROR] {e}")

    def player_size(self):
        return str(len(self.clients))

    def get_max_connection(self):
        return self.max_connection

    def debug_clients(self):
        print(self.clients)
        print("Length:",len(self.clients))

    def start(self):
        print(f"Server is starting...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.addr)
        server.listen(self.max_connection)
        print(f"Server is listening on {self.ip}:{self.port}")

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
        
        print(f"[{addr[0]}]  Estabilished connection to server.")
        
        connected = True
        while connected:
            try:
                recv_data_binary = conn.recv(self.size)
            except ConnectionResetError as e:
                print(f"[{addr[0]}] Disconnected")
                print(f"[ERROR] {e}")
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

            self.notify(recv_data, conn)
            # if "><" in recv_data:
            #     recv_data = recv_data[recv_data.index("><")+2:]
            # if recv_data == "get_player_size":
            #     return_message = str(self.player_size()) +"," + str(self.get_max_connection())
            #     self.send_to_client(conn, return_message)
            #     print("<<< Sending size", return_message)
            # self.broadcast_message(recv_data)

                
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
    
    
class GameLogic(Observer):
    def __init__(self, max_players):
        super(GameLogic, self).__init__()
        self.state = "WAITING"
        self.max_players = max_players
        pass

    def update(self, new_value):
        print(f"Game Logic handles message: {new_value[0]} by {new_value[1]}")
        global server_ref
        global qna_ref
        
        recv_data = new_value[0]
        conn = new_value[1]
        
        match self.state:
            case "WAITING":
                if "><" in recv_data:
                    recv_data = recv_data[recv_data.index("><")+2:]
                if recv_data == "get_player_size":
                    return_message = str(self.player_size()) +"," + str(self.get_max_connection())
                    self.send_to_client(conn, return_message)
                    print("<<< Sending size", return_message)
                server_ref.broadcast_message(recv_data)
                server_ref.broadcast_message(qna_ref.get_random_qna(7))
            case "ONGOING":
                pass
            case _:
                pass
            
                
        
        

    

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

def get_server():
    global server_ref
    size = server_ref.player_size()
    return size

def set_server_ref(obj):
    global server_ref
    server_ref = obj

def server_start(max_players=4):
    global server_ref
    global qna_ref
    gamelogic_obj = GameLogic(max_players)
    qna_obj = QuestionAnswerContainer()
    server_obj = Server(max_connection=max_players)
    server_ref = server_obj
    qna_ref = qna_obj
    # set_server_ref(server_obj)
    qna_obj.read_from_file()
    server_obj.attach(gamelogic_obj)
    
    server_obj.start()
    
