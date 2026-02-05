import time

_cache = {}

def get_cache(key):
    entry = _cache.get(key)
    if not entry:
        return None

    value, expires_at = entry
    if time.time() > expires_at:
        del _cache[key]
        return None

    return value


def set_cache(key, value, ttl=300):
    expires_at = time.time() + ttl
    _cache[key] = (value, expires_at)