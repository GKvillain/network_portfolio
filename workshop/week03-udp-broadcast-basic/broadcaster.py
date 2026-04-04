import socket
from config import BROADCAST_IP, PORT

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow broadcast packets
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = "DISCOVERY: Who is online?"

    try:
        print(f"[BROADCASTER] Sending to {BROADCAST_IP}:{PORT}")
        print(f"[BROADCASTER] Message: {message}")

        sock.sendto(message.encode(), (BROADCAST_IP, PORT))

        print("[BROADCASTER] Message sent successfully")

    except Exception as e:
        print(f"[BROADCASTER] Error: {e}")

    finally:
        sock.close()
        print("[BROADCASTER] Socket closed")


if __name__ == "__main__":
    main()