# message_queue.py

import time
from collections import deque


class MessageQueue:
    def __init__(self):
        self.queue = deque()

    def add_message(self, message, peer_port):
        msg = {
            "message": message,
            "peer": peer_port,
            "timestamp": time.time()
        }
        self.queue.append(msg)

    def get_messages(self):
        # Return a copy to avoid modifying while iterating
        return list(self.queue)

    def remove_message(self, msg):
        try:
            self.queue.remove(msg)
        except ValueError:
            pass

    def size(self):
        return len(self.queue)