from datetime import datetime

def log_event(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted = f"[{timestamp}] [{level}] {message}"
    print(formatted)

    # Save to file (persistent logging)
    with open("server.log", "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def log_info(message):
    log_event("INFO", message)

def log_error(message):
    log_event("ERROR", message)