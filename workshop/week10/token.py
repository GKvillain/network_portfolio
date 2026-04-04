# token.py

import time
from config import TOKEN_EXPIRY


class Token:
    def __init__(self, message):
        self.message = message
        self.read = False
        self.timestamp = time.time()

    def is_expired(self):
        return (time.time() - self.timestamp) > TOKEN_EXPIRY

    def read_token(self):
        """
        One-time-read enforcement (state collapse)
        """
        if self.read:
            return None

        if self.is_expired():
            return None

        self.read = True
        return self.message

    def __repr__(self):
        status = "READ" if self.read else "UNREAD"
        return f"<Token {status}: '{self.message}'>"