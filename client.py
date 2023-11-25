import socket
import threading
import pickle

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


all_players = []

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
            
            if b'SERIALIZED:' in msg:
                temp = msg.replace(b'SERIALIZED:','')
                temp = pickle.loads(bytes(temp))
                print(temp)
            
        except ConnectionAbortedError:
            print(f"Disconnected from server")
            break
        except ConnectionResetError:
            print(f"[ERROR] Server closed unexpectedly. Check server status.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break

def main():
    pname = "PNAME:" + str(input("Player Name: "))
    
    
    # Client initialization
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[THIS CLIENT] Connected to server at {IP}:{PORT}")

    # Handle server incoming msg
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    
    # Send player information
    try:
        client.send(pname.encode(FORMAT))
    except Exception as e:
        print(f"[ERROR] {e}")
            

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