import socket
import pickle
import random
import threading
from game import Game
from questions import Q_and_A

server_ref = None

class Server:
    def __init__(self, port = 5566, size = 4096, max_connection = 4) -> None:
        self.ip = self.get_ip()
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = size
        self.format = "utf-8"
        self.server_id = (f"[Server {socket.gethostname()} ({self.ip}:{self.port})]")
        self.max_connection = max_connection
        
        self.clients: dict[str,socket.socket] = {}
        self.clients_lock = threading.Lock()

        self.games: dict[int,Game] = {}
        self.id_generator = IdGenerator()

        self.start()

    def player_size(self):
        return len(self.clients)

    def debug_clients(self):
        print(self.clients)
        print("Length:",len(self.clients))

    def start(self):
        print(f"{self.server_id} Server is starting...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(self.addr)
            server.listen()
        except:
            print(f"{self.server_id} Server failed to start. Port {self.port} is currently in use by another process.")
            return
        print(f"{self.server_id} Server is listening on {self.ip}:{self.port}")

        while True: 
            conn, addr = server.accept()
            self.clients[addr[0]] = conn
            print("Connected to:", addr)
            thread = threading.Thread(target=self.threaded_client, args=(conn,addr))
            thread.start()
    
    def threaded_client(self, conn:socket.socket, addr):
        try:
            game_id = 0
            joined = False
            
            while not joined:
                try:
                    data = conn.recv(2048).decode().split(',')
                    if isinstance(data,list) and len(data) > 1:
                        print('yes list')
                        # ipv4 address is used as player id
                        player_ip = data[2]
                        name = data[3]
                        game = None

                        # Create a game
                        if data[0] == 'create':
                            print('create requested')     
                            if len(self.games) < 6:
                                player_size = data[1]
                                game_id = self.id_generator.generate()
                                self.games[game_id] = Game(game_id, player_size)
                                print("Creating a new game...")
                                game = self.games[game_id]

                                # Add a player with an initial score of 0
                                # to the dict of players in the new game
                                game.add_player(player_ip, name, 0)
                                joined = True
                                print(f"{name} [{player_ip}] has joined Game {game_id}")

                                # Shuffle Q_and_A then use the first 10
                                random.shuffle(Q_and_A)
                                game.set_qna(Q_and_A[:10])
                            else: 
                                conn.sendall(pickle.dumps('max games reached'))
                        # Join a game
                        elif data[0] == 'join':
                            print('join requested')   
                            game_id = int(data[1])
                            game = self.games[game_id]
                            if game.get_player_count() < game.get_player_size():
                                game.add_player(player_ip, name, 0)
                                joined = True
                                print(f"{player_ip} has joined Game {game_id}")
                                if game.get_player_size() == game.get_player_count():
                                    game.set_start()
                            else:
                                conn.sendall(pickle.dumps("game is full"))

                    # Fetch games requested (view games screen)
                    else:
                        conn.sendall(pickle.dumps(self.games))
        
                except Exception as e:
                    print(f"Error: {e}")
                    break

            print('joined')
            # Send Game object to all players
            try:
                # self.send_game(game)
                conn.sendall(pickle.dumps(game))
                print('game sent')
            except socket.error as e:
                print(e)

            player_count = game.get_player_count()
            data = False
            while not game.has_started():
                try:
                    data = conn.recv(2048).decode()
                    if not data:
                        break
                    if player_count != game.get_player_count():
                        conn.sendall(pickle.dumps(game))
                    else: conn.sendall(pickle.dumps(''))
                except socket.error as e:
                    print(f"Client disconnected: {e}")

            # if not data: 
            #     del self.clients[addr[0]]
            #     print(f'{addr[0]} has disconnected')
            #     conn.close()

            # Game propersdfsdf
            while game.has_started():
                try:
                    data = conn.recv(2048*2).decode()


                    if not data:
                        break 
                    
                except: 
                    break

        finally:
            if game_id != 0 and game.get_player_count() <= 1:
                try: 
                    del self.games[game_id]
                    print(f'Closing Game {game_id}')
                except: pass

                # hey, delete disconnected player from players list

            del self.clients[addr[0]]
            print(f'{addr[0]} has disconnected')
            conn.close()


    def send_game(self, game:Game):
        for client in game.players.keys():
            try:
                conn = self.clients[client]
                conn.sendall(pickle.dumps(game))
            except Exception as e:
                print(f"[ERROR] {e}")


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
            print(self.debug_clients())
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

def get_server():
    global server_ref
    size = server_ref.player_size()
    return size

def set_server_ref(obj):
    global server_ref
    server_ref = obj

def server_start(max_players=4):
    global server_ref
    server_obj = Server(max_connection=max_players)
    server_ref = server_obj
    #set_server_ref(server_obj)
    # testing connection first before game, will uncomment after    #qna_obj = QuestionAnswerContainer()
    #qna_obj.read_from_file()
    
    server_obj.start()

    
"""
if __name__ == "__main__":
    #main(max_players=sys.argv[1])
    main(max_players=4)"""

class IdGenerator:
    def __init__(self, start_range=1, end_range=100):
        self.start_range = start_range
        self.end_range = end_range
        self.generated_ids = set()

    def generate(self):
        while True:
            new_id = random.randint(self.start_range, self.end_range)
            if new_id not in self.generated_ids:
                self.generated_ids.add(new_id)
                return new_id
            
server = Server()