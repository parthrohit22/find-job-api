import time

_cache: dict = {}


def get_cache(key: str):
    entry = _cache.get(key)
    if entry is None:
        return None

    value, expires_at = entry

    if time.time() > expires_at:
        _cache.pop(key, None)
        return None

    return value


def set_cache(key: str, value, ttl: int = 300) -> None:
    expires_at = time.time() + ttl
    _cache[key] = (value, expires_at)