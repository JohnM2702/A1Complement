import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
        except Exception as e:
            print(f"[ERROR] {e}")
            break

def main():
    # Client initialization
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    # Handle server incoming msg
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    connected = True
    while connected:
        try:
            msg = input("> ")
            client.send(msg.encode(FORMAT))
        except Exception as e:
            print(f"[ERROR] {e}")
            break

        if msg == DISCONNECT_MSG:
            connected = False
            
    client.close()


if __name__ == "__main__":
    main()