# config.py

HOST = "127.0.0.1"

# Change this per node when running multiple instances
BASE_PORT = 8000  

# Peers (adjust depending on which node you're running)
PEER_PORTS = [8001, 8002]

BUFFER_SIZE = 1024

# Retry interval (seconds)
RETRY_INTERVAL = 5