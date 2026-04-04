import socket
import threading
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE

peer_id = int(sys.argv[1])
PORT = BASE_PORT + peer_id

# ________________________________________
# Step 2: Listener Thread
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent "Address already in use" error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[PEER {peer_id}] Listening on {PORT}")

    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(BUFFER_SIZE)

            if data:
                print(f"\n[PEER {peer_id}] From {addr}: {data.decode()}")
            
            conn.close()

        except Exception as e:
            print(f"[PEER {peer_id}] Listener error: {e}")

# ________________________________________
# Step 3: Sender Function
def send_message(target_peer_id, message):
    target_port = BASE_PORT + target_peer_id

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, target_port))

        sock.sendall(message.encode())
        sock.close()

    except ConnectionRefusedError:
        print(f"[PEER {peer_id}] ERROR: Peer {target_peer_id} is not running")

    except Exception as e:
        print(f"[PEER {peer_id}] Send error: {e}")

# ________________________________________
# Step 4: Run Listener + Send Message
threading.Thread(target=listen, daemon=True).start()

while True:
    try:
        target = int(input("\nSend to peer ID: "))
        msg = input("Message: ")

        send_message(target, msg)

    except ValueError:
        print("[ERROR] Please enter a valid peer ID")

    except KeyboardInterrupt:
        print("\n[PEER] Shutting down...")
        break