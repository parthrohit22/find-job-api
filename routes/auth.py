from flask import Blueprint, request

from services.user_store import authenticate_user, create_user
from utils.auth import is_legacy_api_key, preview_api_key


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True) or {}

    try:
        user = create_user(
            name=payload.get("name", ""),
            email=payload.get("email", ""),
            password=payload.get("password", ""),
        )
    except ValueError as exc:
        message = str(exc)
        status_code = 409 if "already exists" in message.lower() else 400
        return {"error": message}, status_code

    return {
        "message": "account created",
        "apiKey": user["apiKey"],
        "user": {
            "name": user["name"],
            "email": user["email"],
            "keyPreview": user["keyPreview"],
        },
    }, 201


@auth_bp.route("/auth/login", methods=["POST"])
@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}

    legacy_api_key = (payload.get("apiKey") or "").strip()
    if legacy_api_key:
        if not is_legacy_api_key(legacy_api_key):
            return {"error": "invalid API key"}, 401

        name = (payload.get("name") or "Legacy User").strip() or "Legacy User"
        return {
            "message": "authenticated",
            "apiKey": legacy_api_key,
            "user": {
                "name": name[:60],
                "email": "legacy@example.local",
                "keyPreview": preview_api_key(legacy_api_key),
            },
        }

    try:
        user = authenticate_user(
            email=payload.get("email", ""),
            password=payload.get("password", ""),
        )
    except ValueError as exc:
        return {"error": str(exc)}, 400
    except PermissionError as exc:
        return {"error": str(exc)}, 401

    return {
        "message": "authenticated",
        "apiKey": user["apiKey"],
        "user": {
            "name": user["name"],
            "email": user["email"],
            "keyPreview": user["keyPreview"],
        },
    }
