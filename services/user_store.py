from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path
import os
import sqlite3

from utils.auth import (
    generate_api_key,
    gensalt,
    preview_api_key,
    sha256_with_salt,
    verify_sha256_with_salt,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "jobsearch.sqlite3"
DB_PATH = Path(os.getenv("USER_DB_PATH", DEFAULT_DB_PATH))
API_KEY_PREFIX_LENGTH = 18


def init_user_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                api_key_hash TEXT NOT NULL,
                api_key_salt TEXT NOT NULL,
                api_key_prefix TEXT NOT NULL,
                api_key_preview TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                last_login_at TEXT
            )
            """
        )
        connection.commit()


def create_user(name: str, email: str, password: str) -> dict:
    normalized_name = _validate_name(name)
    normalized_email = _validate_email(email)
    _validate_password(password)

    password_salt = gensalt()
    password_hash = sha256_with_salt(password, password_salt)
    api_key = generate_api_key()
    api_key_salt = gensalt()
    api_key_hash = sha256_with_salt(api_key, api_key_salt)
    api_key_preview = preview_api_key(api_key)
    api_key_prefix = api_key[:API_KEY_PREFIX_LENGTH]
    timestamp = _now()

    with _connect() as connection:
        existing_user = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()

        if existing_user:
            raise ValueError("An account with that email already exists.")

        connection.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash,
                password_salt,
                api_key_hash,
                api_key_salt,
                api_key_prefix,
                api_key_preview,
                created_at,
                updated_at,
                last_login_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalized_name,
                normalized_email,
                password_hash,
                password_salt,
                api_key_hash,
                api_key_salt,
                api_key_prefix,
                api_key_preview,
                timestamp,
                timestamp,
                timestamp,
            ),
        )
        connection.commit()

    return {
        "name": normalized_name,
        "email": normalized_email,
        "apiKey": api_key,
        "keyPreview": api_key_preview,
    }


def authenticate_user(email: str, password: str) -> dict:
    normalized_email = _validate_email(email)
    _validate_password(password)

    with _connect() as connection:
        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                password_salt
            FROM users
            WHERE email = ?
            """,
            (normalized_email,),
        ).fetchone()

        if not user:
            raise PermissionError("Invalid email or password.")

        if not verify_sha256_with_salt(password, user["password_salt"], user["password_hash"]):
            raise PermissionError("Invalid email or password.")

        api_key = generate_api_key()
        api_key_salt = gensalt()
        api_key_hash = sha256_with_salt(api_key, api_key_salt)
        api_key_preview = preview_api_key(api_key)
        api_key_prefix = api_key[:API_KEY_PREFIX_LENGTH]
        timestamp = _now()

        connection.execute(
            """
            UPDATE users
            SET api_key_hash = ?,
                api_key_salt = ?,
                api_key_prefix = ?,
                api_key_preview = ?,
                updated_at = ?,
                last_login_at = ?
            WHERE id = ?
            """,
            (
                api_key_hash,
                api_key_salt,
                api_key_prefix,
                api_key_preview,
                timestamp,
                timestamp,
                user["id"],
            ),
        )
        connection.commit()

    return {
        "name": user["name"],
        "email": user["email"],
        "apiKey": api_key,
        "keyPreview": api_key_preview,
    }


def find_user_by_api_key(api_key: str) -> dict | None:
    normalized_api_key = (api_key or "").strip()
    if not normalized_api_key:
        return None

    api_key_prefix = normalized_api_key[:API_KEY_PREFIX_LENGTH]

    with _connect() as connection:
        candidate_users = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                api_key_hash,
                api_key_salt,
                api_key_preview
            FROM users
            WHERE api_key_prefix = ?
            """,
            (api_key_prefix,),
        ).fetchall()

    for user in candidate_users:
        if verify_sha256_with_salt(normalized_api_key, user["api_key_salt"], user["api_key_hash"]):
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "keyPreview": user["api_key_preview"],
            }

    return None


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _validate_name(name: str) -> str:
    normalized_name = (name or "").strip()
    if len(normalized_name) < 2:
        raise ValueError("Name must be at least 2 characters long.")

    return normalized_name[:80]


def _validate_email(email: str) -> str:
    normalized_email = (email or "").strip().lower()
    if not normalized_email or "@" not in normalized_email or "." not in normalized_email:
        raise ValueError("Enter a valid email address.")

    return normalized_email[:160]


def _validate_password(password: str) -> str:
    normalized_password = (password or "").strip()
    if len(normalized_password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    return normalized_password
