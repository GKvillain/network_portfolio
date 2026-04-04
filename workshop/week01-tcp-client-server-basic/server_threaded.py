import socket
from concurrent.futures import ThreadPoolExecutor
from config import HOST, PORT, BUFFER_SIZE, TIMEOUT, ENCODING, DELIMITER
from logger import log_info, log_error

MAX_WORKERS = 10

def handle_client(conn, addr):
    log_info(f"Connection from {addr}")
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
        log_info(f"Received from {addr}: {message}")

        if not message:
            reply = "ERROR: Empty message"
        else:
            reply = f"ACK: {message} (Threaded)"

        conn.sendall((reply + DELIMITER).encode(ENCODING))
        log_info(f"Sent reply to {addr}")

    except socket.timeout:
        log_error(f"Timeout from {addr}")
    except Exception as e:
        log_error(f"Error handling {addr}: {e}")
    finally:
        conn.close()
        log_info(f"Closed connection with {addr}")

def start_threaded_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        log_info(f"Threaded server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            executor.submit(handle_client, conn, addr)

    except KeyboardInterrupt:
        log_info("Server shutting down...")
    finally:
        server_socket.close()
        executor.shutdown(wait=True)
        log_info("Server stopped cleanly.")

if __name__ == "__main__":
    start_threaded_server()