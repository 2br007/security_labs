import time
from collections import defaultdict
from typing import Dict


class RateLimiter:
    """
    Simple in-memory rate limiter.

    NOTE:
        For production use Redis or API gateway (NGINX, Kong).
    """

    def __init__(self, limit: int = 5, window_seconds: int = 60):
        self.limit = limit
        self.window = window_seconds
        self.requests: Dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        timestamps = self.requests[key]

        # remove expired requests
        self.requests[key] = [t for t in timestamps if now - t < self.window]

        if len(self.requests[key]) >= self.limit:
            return False

        self.requests[key].append(now)
        return True
