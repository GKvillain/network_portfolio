# config.py

HOST = "127.0.0.1"

# 👉 Change this per node before running
BASE_PORT = 11000

# Example peers (adjust depending on node)
PEER_PORTS = [11001, 11002]

BUFFER_SIZE = 1024

# Token expires after this many seconds
TOKEN_EXPIRY = 10

# How often node tries to forward tokens
UPDATE_INTERVAL = 3