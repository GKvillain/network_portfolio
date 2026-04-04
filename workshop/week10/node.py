# node.py

import socket
import threading
import time
import random

from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, UPDATE_INTERVAL
from token import Token

# Local storage of tokens
token_queue = []

# -------------------------
# SEND TOKEN
# -------------------------
def send_token(peer_port, token):
    if token.is_expired():
        print(f"[NODE {BASE_PORT}] Token expired before sending")
        return False

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))

        # Send only message (conceptual limitation)
        s.sendall(token.message.encode())

        s.close()
        print(f"[NODE {BASE_PORT}] Sent token to {peer_port}")
        return True

    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] Failed to send to {peer_port}")
        return False


# -------------------------
# FORWARD LOOP
# -------------------------
def forward_loop():
    while True:
        for token in token_queue[:]:

            # Remove expired tokens
            if token.is_expired():
                print(f"[NODE {BASE_PORT}] Removing expired token: {token.message}")
                token_queue.remove(token)
                continue

            # Probabilistic forwarding (quantum-like uncertainty)
            if random.random() < 0.5:
                continue

            # Try sending to peers
            for peer in PEER_PORTS:
                success = send_token(peer, token)
                if success:
                    token_queue.remove(token)
                    break

        time.sleep(UPDATE_INTERVAL)


# -------------------------
# SERVER (RECEIVE TOKENS)
# -------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()

        try:
            data = conn.recv(BUFFER_SIZE).decode()

            token = Token(data)

            # Attempt to read (collapse happens here)
            message = token.read_token()

            if message:
                print(f"[NODE {BASE_PORT}] Received token: {message}")
                token_queue.append(token)
            else:
                print(f"[NODE {BASE_PORT}] Invalid or expired token")

        except Exception as e:
            print(f"[NODE {BASE_PORT}] Error: {e}")

        finally:
            conn.close()


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":

    # Start server thread
    threading.Thread(target=start_server, daemon=True).start()

    # Start forwarding thread
    threading.Thread(target=forward_loop, daemon=True).start()

    # Initial token injection
    initial_token = Token(f"Quantum token from {BASE_PORT}")
    token_queue.append(initial_token)

    print(f"[NODE {BASE_PORT}] Started with initial token")

    # Keep alive
    while True:
        time.sleep(1)