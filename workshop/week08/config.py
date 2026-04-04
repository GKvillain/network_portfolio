# config.py
HOST = "127.0.0.1"
BASE_PORT = 9000  # Change per node instance (9000, 9001, 9002...)
PEER_PORTS = [9001, 9002]  # Update per node

BUFFER_SIZE = 1024

FORWARD_THRESHOLD = 0.5
UPDATE_INTERVAL = 5  # seconds