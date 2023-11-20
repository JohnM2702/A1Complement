import socket
import threading
from gamestate import GameState

# Server Configurations
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

clients = []
clients_lock = threading.Lock()

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
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f"[{addr}] {msg}")
            msg = f"Msg received: {msg}"
            conn.send(msg.encode(FORMAT))
            forward_message(addr, msg)
        except Exception as e:
            print(f"[ERROR] {e}")
            break
        
    with clients_lock:
        # Remove the disconnected client from the clients list
        clients[:] = [client for client in clients if client["address"] != addr]

    conn.close()

game = GameState(5)
def main():
    # Server initialization
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    


    while True:
        conn, addr = server.accept()
        client_info = {"connection": conn, "address": addr}
        with clients_lock:
            clients.append(client_info)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()