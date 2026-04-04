import socket
from config import HOST, PORT

def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message.encode(), (HOST, PORT))
    print(f"[SENDER] Sent: {message}")

    sock.close()

if __name__ == "__main__":
    msg = input("Enter message: ")
    send_message(msg)