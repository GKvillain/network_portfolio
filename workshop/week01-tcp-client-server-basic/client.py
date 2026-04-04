import socket
from config import HOST, PORT, BUFFER_SIZE, TIMEOUT, ENCODING, DELIMITER

def send_message(message):
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        client_socket.connect((HOST, PORT))

        full_message = message + DELIMITER
        print(f"[CLIENT] Sending: {message}")
        client_socket.sendall(full_message.encode(ENCODING))

        # Receive full response (stream-safe)
        data = b""
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
            if DELIMITER.encode() in data:
                break

        response = data.decode(ENCODING).strip()
        print(f"[CLIENT] Received: {response}")

    except Exception as e:
        print(f"[CLIENT] Error: {e}")
    finally:
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello Advanced Server"
    send_message(msg)