# sender.py

import socket
import time
from config import MULTICAST_GROUP, PORT, TTL


def create_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set multicast TTL (scope control)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

    return sock


def send_once(sock, message):
    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
    print(f"[SENDER] Sent: {message}")


def send_periodic(sock, interval=2):
    count = 1
    try:
        while True:
            message = f"MULTICAST #{count}"
            send_once(sock, message)
            count += 1
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[SENDER] Stopped.")


def main():
    sock = create_sender()

    print("[SENDER] Choose mode:")
    print("1. Send once")
    print("2. Send periodically")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        message = input("Enter message: ")
        send_once(sock, message)

    elif choice == "2":
        interval = input("Interval (seconds): ").strip()
        interval = int(interval) if interval.isdigit() else 2
        send_periodic(sock, interval)

    else:
        print("[SENDER] Invalid choice")

    sock.close()


if __name__ == "__main__":
    main()