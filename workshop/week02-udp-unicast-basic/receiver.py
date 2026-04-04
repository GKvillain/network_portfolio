import socket
from config import HOST, PORT, BUFFER_SIZE

def start_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"[RECEIVER] Listening on {HOST}:{PORT}")

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f"[RECEIVER] From {addr}: {data.decode()}")

    except KeyboardInterrupt:
        print("\n[RECEIVER] Shutting down...")
    finally:
        sock.close()

if __name__ == "__main__":
    start_receiver()