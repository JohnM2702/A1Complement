import socket
import pickle
import random
import threading
from game import Game
from time import sleep
from questions import Q_and_A

class Server:
    def __init__(self) -> None:
        self.ip = self.get_ip()
        self.port = 5566
        self.addr = (self.ip, self.port)
        self.size = 2048
        self.format = "utf-8"
        
        self.clients: dict[str,socket.socket] = {}
        self.clients_lock = threading.Lock()

        self.games: dict[int,Game] = {}
        self.id_generator = IdGenerator()

        self.start()

    def debug_clients(self):
        print(self.clients)
        print("Length:",len(self.clients))

    def start(self):
        print(f"Server is starting...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.addr)
        server.listen()
        print(f"Server is listening on {self.ip}:{self.port}")

        while True: 
            conn, addr = server.accept()
            self.clients[addr[0]] = conn
            print("Connected to:", addr)
            thread = threading.Thread(target=self.threaded_client, args=(conn,addr))
            thread.start()
    
    def create_game(self, data):
        player_size = data[1]
        ip = data[2]
        name = data[3]
        game_id = self.id_generator.generate()
        
        self.games[game_id] = Game(game_id, player_size)
        print(f'Game {game_id} has been successfully created')
        game = self.games[game_id]

        # Add the client, with an initial score of 0, 
        # to the dict of players in the newly created game
        game.add_player(ip, name, 0)
        print(f"{ip} has joined Game {game_id}")

        # Shuffle Q_and_A, then take the first 10 questions & answers
        random.shuffle(Q_and_A)
        game.set_qna(Q_and_A[:10])
        
        return game, game_id
        
    def join_game(self, game, game_id, data):
        ip = data[2]
        name = data[3]
        game.add_player(ip, name, 0)
        print(f"{ip} has joined Game {game_id}")
        if game.get_player_size() == game.get_player_count():
            game.set_start()
    
    
    def threaded_client(self, conn:socket.socket, addr):
        game = None 
        try:
            # PREGAME: client will either create a new game,
            # view existing games, or join a game
            game, game_id = self.handle_pregame(conn)

            # Client has joined a game, so send them the Game object
            conn.sendall(pickle.dumps(game))
            
            # Client will now wait for other players to join
            self.handle_waiting(conn,game)
            
            # Play the actual game
            self.handle_game(conn,game,addr[0])
        
        except socket.error as e:
            print(f"ERROR: {e}")
        
        except Exception as e:
            print(f"ERROR: {e}")
        
        finally: 
            if game is not None:
                # Delete the player from the list of players in the Game object
                game.delete_player(addr[0])
                player_count = game.get_player_count()
                # Delete the game if there is only 1 or no players left
                if (player_count <= 1 and game.has_started()) or player_count == 0:
                    try: 
                        del self.games[game_id]
                        print(f'Deleting Game {game_id}')
                    except: pass
            # Delete the client from the list of clients in the server
            del self.clients[addr[0]]
            print(f'{addr[0]} has disconnected')
            conn.close()
    
    
    def handle_pregame(self, conn: socket.socket) -> tuple[Game,int]:
        while True:
            data = conn.recv(2048).decode().split(',')
    
            if data[0] == 'create':
                print('create request received')     
                if len(self.games) < 6:
                    return self.create_game(data)
                else: 
                    conn.sendall(pickle.dumps('max games reached'))
                    
            elif data[0] == 'join':
                print('join request received')   
                game_id = int(data[1])
                game = self.games[game_id]
                if game.get_player_count() < game.get_player_size():
                    self.join_game(game,game_id,data)
                    return game, game_id
                else: 
                    conn.sendall(pickle.dumps("game is full"))

            # Fetch games requested ('view games' screen)
            else: conn.sendall(pickle.dumps(self.games))
    
    def handle_waiting(self, conn: socket.socket, game: Game):
        player_count = game.get_player_count()
        while not game.has_started():
            data = conn.recv(2048).decode()
            if not data: raise socket.error('lost connection')
            
            updated_count = game.get_player_count()
            if player_count != updated_count or player_count > updated_count:
                # Another client has joined the game, so send updated Game to client
                conn.sendall(pickle.dumps(game))
                player_count = updated_count
            else: conn.sendall(pickle.dumps(''))
    
    def handle_game(self, conn: socket.socket, game: Game, ip: str):
        index = 0
        while True:
            time_limit = 10000
            
            # Send index of next question
            self.handle_round_transition(conn,game,index,ip)
            
            # data = conn.recv(2048).decode().split(',')
            # if not data: raise socket.error('lost connection')
        
            # elif data[0] == 'index':
            #     print(f'index request received from {ip}')
            #     conn.sendall(pickle.dumps(index))
            #     game.increment_sent_index()
            # else: conn.sendall(pickle.dumps(''))
            
            # print(f'wow {data} from {ip}')
            
            # # print(str(data))
            # # print(index)
            # while True:
            #     if game.count_sent_index() == game.get_player_count(): break
            
            print(f'round {index} start {ip}')
            while not game.is_round_finished(index):
                data = conn.recv(2048).decode().split(',')
                if not data: 
                    raise socket.error('lost connection')
                elif data[0] == 'add time':
                    time_limit += 5000
                    conn.sendall(pickle.dumps(time_limit))
                elif data[0] == 'subtract time':
                    self.broadcast_with_exclusion('subtract 3000',ip)
                elif data[0] == 'disable hint':
                    self.broadcast_with_exclusion('disable hint',ip)
                elif data[0] == 'score':
                    print(f'score received: {data[1]} from {ip}')
                    game.update_score(ip,int(data[1]),index)
                    self.broadcast_message(game)
                else:
                    conn.sendall(pickle.dumps(''))
                
            print(f'Round {index} is over, {ip}')
            
            # data = conn.recv(2048).decode()
            # if not data: raise socket.error('lost connection')
            # print(f'{data} from {ip}')
            
            # conn.sendall(pickle.dumps('next round'))
            
            index += 1
            if index == game.get_qna_length():
                print('Game Over')
                break
    
    
    def handle_round_transition(self, conn:socket.socket, game:Game, index:int, ip:str):
        data = conn.recv(2048).decode()
        if not data: raise socket.error('lost connection')
        elif 'index' in data:
            print(f'index request received from {ip}')
            conn.sendall(pickle.dumps(index))
            game.increment_sent_index()
        # else: conn.sendall(pickle.dumps(''))
        
        print(f'wow {data} from {ip}')

        while True:
            if game.count_sent_index() == game.get_player_count(): return
            
    def broadcast_with_exclusion(self, message, excluded):
        for ip, client in self.clients.items():
            if ip is not excluded:
                try:
                    client.sendall(pickle.dumps(message))
                except Exception as e:
                    print(f"[ERROR] {e}")
                    
    def broadcast_message(self, message):
        for ip, client in self.clients.items():
            try:
                client.sendall(pickle.dumps(message))
            except Exception as e:
                print(f"[ERROR] {e}")
                
    # def send_game(self, game, ip, conn):
    #     try:
    #         conn.sendall(pickle.dumps(game))
    #     except socket.error as e:
    #         print(f"ERROR: {e}")
    #         self.handle_disconnection(game,game.get_id(),ip,conn)

    # def handle_disconnection(self, game, game_id, ip, conn):
    #     if game is not None:
    #         game.delete_player(ip)
    #         player_count = game.get_player_count()
    #         if (player_count <= 1 and game.has_started()) or player_count == 0:
    #             try: 
    #                 del self.games[game_id]
    #                 print(f'Deleting Game {game_id}')
    #             except: pass
            
    #     del self.clients[ip]
    #     print(f'{ip} has disconnected')
    #     conn.close()

    # def send_game_to_all(self, game:Game):
    #     for client in game.players.keys():
    #         try:
    #             conn = self.clients[client]
    #             conn.sendall(pickle.dumps(game))
    #         except Exception as e:
    #             print(f"[ERROR] {e}")

    # def broadcast_message(self, message):
    #     for client in self.clients:
    #         try:
    #             if isinstance(message, str):
    #                 data = message.encode(self.format)
    #             else:
    #                 data = pickle.dumps(message)
    #             client["connection"].sendall(data)
    #         except Exception as e:
    #             print(f"[ERROR] {e}")    

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
