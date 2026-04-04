# node.py

import socket
import threading
import time

from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL
from delivery_table import DeliveryTable


delivery_table = DeliveryTable()

# Thread-safe queue + dedup
message_queue = []
seen_messages = set()
lock = threading.Lock()


# ----------------------------
# SEND MESSAGE
# ----------------------------
def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()

        print(f"[NODE {BASE_PORT}] Sent -> {peer_port}: {message}")
        return True

    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] Failed to reach {peer_port}")
        return False


# ----------------------------
# FORWARD LOOP (CORE LOGIC)
# ----------------------------
def forward_loop():
    while True:
        candidates = delivery_table.get_best_candidates(FORWARD_THRESHOLD)

        with lock:
            queue_copy = message_queue[:]

        for msg in queue_copy:
            for peer in candidates:
                success = send_message(peer, msg)

                if success:
                    with lock:
                        if msg in message_queue:
                            message_queue.remove(msg)
                    break  # stop trying other peers

        time.sleep(UPDATE_INTERVAL)


# ----------------------------
# SERVER (RECEIVE MESSAGES)
# ----------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()

        if data:
            print(f"[NODE {BASE_PORT}] Received from {addr}: {data}")

            with lock:
                if data not in seen_messages:
                    seen_messages.add(data)
                    message_queue.append(data)
                else:
                    print(f"[NODE {BASE_PORT}] Duplicate ignored")

        conn.close()


# ----------------------------
# OPTIONAL: SIMULATE DYNAMIC PROBABILITY
# ----------------------------
def probability_update_loop():
    import random

    while True:
        for peer in PEER_PORTS:
            new_prob = round(random.uniform(0.3, 0.9), 2)
            delivery_table.update_probability(peer, new_prob)

        print(f"[NODE {BASE_PORT}] Updated probabilities: {delivery_table}")
        time.sleep(UPDATE_INTERVAL)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    # Start server thread
    threading.Thread(target=start_server, daemon=True).start()

    # Start forwarding logic
    threading.Thread(target=forward_loop, daemon=True).start()

    # Start dynamic probability updates (optional but useful)
    threading.Thread(target=probability_update_loop, daemon=True).start()

    # Initialize probabilities (fallback)
    for peer in PEER_PORTS:
        delivery_table.update_probability(peer, 0.6)

    # Initial message send
    for peer in PEER_PORTS:
        msg = f"Hello from node {BASE_PORT}"

        if not send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Storing message (no route)")
            with lock:
                message_queue.append(msg)

    # Keep program alive
    while True:
        time.sleep(1)