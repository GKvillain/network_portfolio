import socket
import threading
import time

from config import (
    HOST, BASE_PORT, PEER_PORTS,
    BUFFER_SIZE, FORWARD_THRESHOLD,
    UPDATE_INTERVAL, REINFORCEMENT
)

from pheromone_table import PheromoneTable

pheromone_table = PheromoneTable()
message_queue = []

# ---------------------------
# SEND MESSAGE
# ---------------------------
def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))

        s.sendall(message.encode())
        s.close()

        print(f"[NODE {BASE_PORT}] Sent → {peer_port}: {message}")

        # ✅ reinforce success
        pheromone_table.reinforce(peer_port, REINFORCEMENT)
        return True

    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] ❌ Failed → {peer_port}")
        return False


# ---------------------------
# FORWARD LOOP
# ---------------------------
def forward_loop():
    while True:
        pheromone_table.decay()

        candidates = pheromone_table.get_best_candidates(FORWARD_THRESHOLD)

        if not candidates:
            print("[FORWARD] No strong paths yet")

        for msg in message_queue[:]:
            for peer in candidates:
                success = send_message(peer, msg)

                if success:
                    message_queue.remove(msg)
                    break  # stop trying other peers

        pheromone_table.debug_print()
        time.sleep(UPDATE_INTERVAL)


# ---------------------------
# SERVER
# ---------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()

        data = conn.recv(BUFFER_SIZE).decode()
        print(f"[NODE {BASE_PORT}] Received ← {addr}: {data}")

        # add to queue for forwarding
        message_queue.append(data)

        conn.close()


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":

    # start server + forwarding threads
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=forward_loop, daemon=True).start()

    # initialize pheromones
    for peer in PEER_PORTS:
        pheromone_table.reinforce(peer, 1.0)

    # initial send
    for peer in PEER_PORTS:
        msg = f"Hello from {BASE_PORT}"
        if not send_message(peer, msg):
            message_queue.append(msg)

    while True:
        time.sleep(1)