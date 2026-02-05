# In real systems, this lives in a database
VALID_API_KEYS = {
    "test-key-123",
    "demo-key-456"
}

def is_valid_api_key(key):
    return key in VALID_API_KEYS