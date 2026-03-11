import time
from collections import defaultdict

_requests = defaultdict(list)


def is_rate_limited(ip: str, limit: int = 20, window: int = 60) -> bool:
    now = time.time()
    window_start = now - window

    _requests[ip] = [t for t in _requests[ip] if t > window_start]

    if len(_requests[ip]) >= limit:
        return True

    _requests[ip].append(now)
    return False