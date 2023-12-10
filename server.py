from q_genknowledge import genknowledge_qna 
from q_networking import networking_qna
from game import Game
import dill as pickle
import threading
import socket
import random

class Server:
    def __init__(self) -> None:
        self.ip = self.get_ip()
        self.port = 5566
        self.addr = (self.ip, self.port)
        self.clients: dict[str,socket.socket] = {}
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
            print("Connected to:", addr)
            self.clients[addr[0]] = conn
            thread = threading.Thread(target=self.threaded_client, args=(conn,addr[0]))
            thread.start()
            
    def create_game(self, data, ip):
        player_size = data[1]
        name = data[2]
        category = data[3]
        game_id = self.id_generator.generate()
        
        self.games[game_id] = Game(game_id, player_size, category)
        print(f'Game {game_id} has been successfully created')
        game = self.games[game_id]

        # Add the client, with an initial score of 0, 
        # to the dict of players in the newly created game
        game.add_player(ip, name)
        print(f"{ip} has joined Game {game_id}")

        qna = None
        if category == 'General Knowledge': qna = genknowledge_qna
        elif category == 'Networking': qna = networking_qna
        random.shuffle(qna)
        game.set_qna(qna[:10])

        return game, game_id
        
    def join_game(self, game:Game, game_id, data, ip):
        name = data[2]
        game.add_player(ip, name)
        print(f"{ip} has joined Game {game_id}")
        if game.get_player_size() == game.get_player_count():
            game.set_start()

    def threaded_client(self, conn:socket.socket, ip):
        try:
            while True:
                game, game_id = None, None

                # PREGAME: client will either create a new game,
                # view existing games, or join a game
                game, game_id = self.handle_pregame(conn,ip)
                
                try:
                    # Client just joined a game, send them the Game object
                    # conn.sendall(pickle.dumps(game))

                    while True:
                        conn.sendall(pickle.dumps(game))
                        print(f'sent initial game to {ip}')
                        data = conn.recv(2048).decode()
                        if not data: raise socket.error('lost connection')
                        if 'received game' in data:
                            print(f'{ip} has received the initial Game')
                            break
                    
                    # WAITING: Wait for other players to join
                    self.handle_waiting(conn,game)
                    
                    # GAME: Play the actual game
                    self.handle_game(conn,game,ip)

                except socket.error as e:
                    print(f"ERROR: {e}")
                finally: 
                    self.delete_player(game,game_id,ip)

        except socket.error as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR: {e}")
        finally: 
            self.handle_disconnection(game,game_id,ip,conn)
    
    def handle_pregame(self, conn: socket.socket, ip) -> tuple[Game,int]:
        while True:
            data = conn.recv(2048).decode().split(',')
            if not data: raise socket.error('lost connection')

            if data[0] == 'create':
                print('create request received')     
                if len(self.games) < 6:
                    return self.create_game(data,ip)
                else: 
                    conn.sendall(pickle.dumps('max games reached'))
                    
            elif data[0] == 'join':
                print('join request received')   
                game_id = int(data[1])
                game = self.games[game_id]
                if game.get_player_count() < game.get_player_size():
                    self.join_game(game,game_id,data,ip)
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
            broadcast_thread = None
            time_limit = 10000
            
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
                    broadcast_thread = threading.Thread(target=self.broadcast_with_exclusion, args=(game,ip))
                    broadcast_thread.start()      
                else:
                    # conn.send(pickle.dumps(''))
                    conn.sendall(pickle.dumps(game))

            print(f'Round {index} is over, {ip}')

            if isinstance(broadcast_thread,threading.Thread):
                broadcast_thread.join()

            while True:
                if game.get_received_count(ip) >= game.get_player_count() - 1:
                    while True:
                        conn.sendall(pickle.dumps('round end'))
                        print(f'sent end notice to {ip}')
                        data = conn.recv(2048).decode()
                        if not data: raise socket.error('lost connection')
                        if 'received notice' in data:
                            print(f'{ip} has received the end notice')
                            break
                    break
            game.reset_received_count(ip)

            index += 1
            if index >= game.get_qna_length():
                print(f'Game {game.get_id()} has ended')
                break

    def broadcast_with_exclusion(self, game:Game, excluded:str):
        for player in game.get_players_except(excluded):
            try:
                self.clients[player].sendall(pickle.dumps(game))
            except Exception as e:
                print(f"[ERROR] {e}")
            game.increment_received_count(player)
            print(f'sent game to {player}')

    def delete_player(self, game:Game, game_id, ip):
        if game is not None:
            # Delete the player from the list of players in the Game object
            game.delete_player(ip)
            player_count = game.get_player_count()
            # Delete the game if there is only 1 or no players left
            if (player_count <= 1 and game.has_started()) or player_count == 0:
                try: 
                    del self.games[game_id]
                    print(f'Deleting Game {game_id}')
                except: pass    # If another client deleted the game first

    def handle_disconnection(self, game:Game, game_id, ip, conn:socket.socket):
        self.delete_player(game,game_id,ip)  
        # Delete the client from the list of clients in the server
        del self.clients[ip]
        print(f'{ip} has disconnected')
        conn.close() 

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
