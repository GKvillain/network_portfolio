import socket
from config import HOST, PORT, BUFFER_SIZE, TIMEOUT, ENCODING, DELIMITER

def handle_client(conn, addr):
    print(f"[SERVER] Connection from {addr}")
    conn.settimeout(TIMEOUT)

    try:
        data = b""
        while True:
            chunk = conn.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
            if DELIMITER.encode() in data:
                break

        message = data.decode(ENCODING).strip()
        print(f"[SERVER] Received: {message}")

        if not message:
            reply = "ERROR: Empty message"
        else:
            reply = f"ACK: {message}"

        conn.sendall((reply + DELIMITER).encode(ENCODING))

    except socket.timeout:
        print(f"[SERVER] Timeout from {addr}")
    except Exception as e:
        print(f"[SERVER] Error: {e}")
    finally:
        conn.close()
        print(f"[SERVER] Closed connection with {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()