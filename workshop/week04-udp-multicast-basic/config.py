# config.py

# Multicast group (must be in 224.0.0.0 – 239.255.255.255)
MULTICAST_GROUP = "224.1.1.1"

# Port to listen/send
PORT = 8000

# Max size of incoming packet
BUFFER_SIZE = 1024

# Time-To-Live (1 = local network only)
TTL = 1