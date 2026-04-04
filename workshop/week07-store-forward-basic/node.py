# node.py

import socket
import threading
import time

from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, RETRY_INTERVAL
from message_queue import MessageQueue

queue = MessageQueue()


# --------------------------------------
# Send Message Function
# --------------------------------------
def send_message(peer_port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((HOST, peer_port))
            s.sendall(message.encode())
        return True
    except (ConnectionRefusedError, socket.timeout):
        return False


# --------------------------------------
# Forward Loop (Retry Stored Messages)
# --------------------------------------
def forward_loop():
    while True:
        messages = queue.get_messages()

        if messages:
            print(f"[NODE {BASE_PORT}] Queue size: {queue.size()}")

        for msg in messages:
            success = send_message(msg["peer"], msg["message"])

            if success:
                print(f"[NODE {BASE_PORT}] Sent stored message to {msg['peer']}")
                queue.remove_message(msg)
            else:
                print(f"[NODE {BASE_PORT}] Retry failed for {msg['peer']}")

        time.sleep(RETRY_INTERVAL)


# --------------------------------------
# Server to Receive Messages
# --------------------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent "address already in use" error
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening for messages...")

    while True:
        conn, addr = server.accept()

        try:
            data = conn.recv(BUFFER_SIZE).decode()
            print(f"[NODE {BASE_PORT}] Received: {data} from {addr}")
        except Exception as e:
            print(f"[NODE {BASE_PORT}] Error receiving data: {e}")

        conn.close()


# --------------------------------------
# Main Execution
# --------------------------------------
if __name__ == "__main__":
    # Start server thread
    threading.Thread(target=start_server, daemon=True).start()

    # Start retry/forward thread
    threading.Thread(target=forward_loop, daemon=True).start()

    time.sleep(1)  # Give server time to start

    # Send initial messages
    for peer in PEER_PORTS:
        message = f"Hello from node {BASE_PORT}"

        if not send_message(peer, message):
            print(f"[NODE {BASE_PORT}] Peer {peer} unavailable, storing message")
            queue.add_message(message, peer)
        else:
            print(f"[NODE {BASE_PORT}] Sent message to {peer}")

    # Keep program running
    while True:
        time.sleep(1)