import socket
from config import PORT, BUFFER_SIZE

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow reuse of the same port by multiple listeners
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Listen on all network interfaces
        sock.bind(("", PORT))

        print(f"[LISTENER] Listening for broadcast messages on port {PORT}")
        print("[LISTENER] Press Ctrl+C to stop\n")

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)

            sender_ip = addr[0]
            sender_port = addr[1]
            message = data.decode()

            print(f"[LISTENER] Received from {sender_ip}:{sender_port}")
            print(f"[LISTENER] Message: {message}")
            print("-" * 50)

    except KeyboardInterrupt:
        print("\n[LISTENER] Stopped by user")

    except Exception as e:
        print(f"[LISTENER] Error: {e}")

    finally:
        sock.close()
        print("[LISTENER] Socket closed")


if __name__ == "__main__":
    main()