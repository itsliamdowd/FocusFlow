import os
from typing import Iterable
from flask import current_app, jsonify, request


def _normalized_roles(raw_roles: str) -> set[str]:
    return {
        role.strip().lower()
        for role in (raw_roles or "").split(",")
        if role and role.strip()
    }


def enforce_api_access(allowed_roles: Iterable[str] | None = None):
    """
    Enforce a minimal API token + role gate on protected routes.

    - `X-API-Token` must match API_AUTH_TOKEN from env.
    - `X-User-Role` must be in allowed_roles when provided.
    """
    expected_token = os.getenv("API_AUTH_TOKEN")
    if not expected_token:
        current_app.logger.error("API_AUTH_TOKEN is not configured")
        return jsonify({"error": "Server authentication is not configured"}), 503

    token = request.headers.get("X-API-Token", "").strip()
    if not token or token != expected_token:
        return jsonify({"error": "Unauthorized"}), 401

    if allowed_roles:
        role = request.headers.get("X-User-Role", "").strip().lower()
        valid_roles = _normalized_roles(",".join(allowed_roles))
        if role not in valid_roles:
            return jsonify({"error": "Forbidden"}), 403

    return None


def enforce_user_scope(requested_user_id):
    """
    Enforce object-level scope for user-owned records.
    Admin role bypasses this check.
    """
    role = request.headers.get("X-User-Role", "").strip().lower()
    if role == "admin":
        return None

    caller_user_id = (request.headers.get("X-User-Id") or "").strip()
    if not caller_user_id:
        return jsonify({"error": "X-User-Id header is required"}), 401

    if str(requested_user_id).strip() != caller_user_id:
        return jsonify({"error": "Forbidden"}), 403
    return None
