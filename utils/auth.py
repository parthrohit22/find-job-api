import hashlib
import hmac
import secrets


LEGACY_VALID_API_KEYS = {
    "test-key-123",
    "demo-key-456",
}


def gensalt(length: int = 16) -> str:
    return secrets.token_hex(length)


def sha256_with_salt(value: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()


def verify_sha256_with_salt(value: str, salt: str, expected_hash: str) -> bool:
    return hmac.compare_digest(sha256_with_salt(value, salt), expected_hash)


def generate_api_key() -> str:
    return f"jobflow_{secrets.token_urlsafe(24)}"


def preview_api_key(key: str) -> str:
    key = key.strip()
    if len(key) <= 4:
        return "*" * len(key)

    return f"{key[:6]}***{key[-4:]}"


def is_legacy_api_key(key: str) -> bool:
    return key in LEGACY_VALID_API_KEYS
