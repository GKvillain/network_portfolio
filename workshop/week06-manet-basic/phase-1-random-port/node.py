import socket
import threading
import random
import sys
import importlib

# -----------------------------
# Load config dynamically
# -----------------------------
def load_node_config():
    try:
        node_idx = int(sys.argv[1])
        cfg = importlib.import_module("config")

        BASE_PORT = cfg.ALL_PORTS[node_idx]
        NEIGHBORS = [p for p in cfg.ALL_PORTS if p != BASE_PORT]

        return BASE_PORT, NEIGHBORS, cfg

    except (IndexError, ValueError):
        print("Usage: python node.py <index>")
        sys.exit(1)


BASE_PORT, NEIGHBORS, cfg = load_node_config()

print(f"[INIT] Node on port {BASE_PORT}")
print(f"[INIT] Neighbors: {NEIGHBORS}")

neighbor_table = set(NEIGHBORS)

# -----------------------------
# Handle incoming messages
# -----------------------------
def handle_incoming(conn, addr):
    try:
        data = conn.recv(cfg.BUFFER_SIZE).decode()
        msg, ttl = data.split('|')
        ttl = int(ttl)

        print(f"[NODE {BASE_PORT}] Received: {msg} (TTL={ttl})")

        # Forward probabilistically
        if ttl > 0 and random.random() < cfg.FORWARD_PROBABILITY:
            forward_message(msg, ttl - 1, exclude=addr[1])

    except Exception as e:
        print(f"[NODE {BASE_PORT}] Error: {e}")

    finally:
        conn.close()

# -----------------------------
# Server
# -----------------------------
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent port reuse crash
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((cfg.HOST, port))
    server.listen()

    print(f"[NODE {port}] Listening...")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_incoming,
            args=(conn, addr),
            daemon=True
        ).start()

# -----------------------------
# Forwarding
# -----------------------------
def forward_message(message, ttl, exclude=None):
    for peer_port in neighbor_table:
        if peer_port == exclude:
            continue

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cfg.HOST, peer_port))
            s.sendall(f"{message}|{ttl}".encode())
            s.close()

        except ConnectionRefusedError:
            print(f"[NODE {BASE_PORT}] Peer {peer_port} unreachable")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    threading.Thread(
        target=start_server,
        args=(BASE_PORT,),
        daemon=True
    ).start()

    import time
    time.sleep(1)

    message = f"Hello from node {BASE_PORT}"
    forward_message(message, cfg.TTL)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n[NODE {BASE_PORT}] Shutdown")
            break