# receiver.py

import socket
import struct
from config import MULTICAST_GROUP, PORT, BUFFER_SIZE

def create_receiver():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple receivers on same machine (IMPORTANT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all interfaces on given port
    sock.bind(("", PORT))

    # Join multicast group
    mreq = struct.pack(
        "4sl",
        socket.inet_aton(MULTICAST_GROUP),
        socket.INADDR_ANY
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


def main():
    sock = create_receiver()
    print(f"[RECEIVER] Listening on {MULTICAST_GROUP}:{PORT}")

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode()
            print(f"[RECEIVER] From {addr}: {message}")

    except KeyboardInterrupt:
        print("\n[RECEIVER] Leaving multicast group...")

        # Leave group properly (clean exit)
        mreq = struct.pack(
            "4sl",
            socket.inet_aton(MULTICAST_GROUP),
            socket.INADDR_ANY
        )
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)

        sock.close()
        print("[RECEIVER] Closed.")


if __name__ == "__main__":
    main()