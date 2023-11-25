import socket
import threading
from time import sleep
from gamestate import GameState
import pickle

# Server Configurations
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SERVER_ID = (f"[Server {socket.gethostname()} ({IP} @ {PORT})]")
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

clients = []
clients_lock = threading.Lock()



def broadcast_message(sender_addr, item):
    for client in clients:
        try:
            msg = pickle.dumps(item)
            client["connection"].sendall(msg)
        except Exception as e:
            print(f"[ERROR] {e}")
            
def broadcast_message(sender_addr, message):
    for client in clients:
        try:
            msg = f"[{sender_addr}] {message}"
            client["connection"].send(msg.encode(FORMAT))
        except Exception as e:
            print(f"[ERROR] {e}")

def forward_message(sender_addr, message):
    for client in clients:
        if client["address"] != sender_addr:
            try:
                msg = f"[{sender_addr}] {message}"
                client["connection"].send(msg.encode(FORMAT))
            except Exception as e:
                print(f"[ERROR] {e}")

def handle_client(conn, addr):
    
    CLIENT_ID = (f"[Client {socket.gethostbyaddr(addr[0])[0]} ({addr[0]} @ {addr[1]})]")
    print(f"{CLIENT_ID}  Estabilished connection to server.")
    
    connected = True
    while connected:
        try:
            msg:str = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                break
            print(f"[{addr[0]}] {msg}")
        except ConnectionResetError:
            print(f"[{addr[0]}] Disconnected")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break
        
        if "PNAME:" in msg:
            game.add_player(msg.replace('PNAME:',''),conn,addr)
            print("ADDED PLAYER")
            
    with clients_lock:
        # Remove the disconnected client from the clients list
        clients[:] = [client for client in clients if client["address"] != addr]

    try:
        conn.close()
    except:
        pass

game = GameState(2)
def main():
    print(f"{SERVER_ID} Server is starting...")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
    except:
        print(f"{SERVER_ID} Server failed to start. Port {PORT} is currently in use by another process.")
        return
    print(f"{SERVER_ID} Server is listening on {IP}:{PORT}")

    while len(clients) < game.player_count:
        conn, addr = server.accept()
        client_info = {"connection": conn, "address": addr}
        with clients_lock:
            clients.append(client_info)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()  
        
    sleep(2)
    print(f"{SERVER_ID} [GAME] All players have connected to the server")
    print(f"{SERVER_ID} [GAME] Game is starting...")
    print(f"{SERVER_ID} [GAME] Players: {game.get_player_names_str()}")
    broadcast_message(SERVER_ID, f"PLIST: {{game.get_player_names_str()}}")
    
    
    
    
    

if __name__ == "__main__":
    main()