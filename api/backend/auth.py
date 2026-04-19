from typing import Iterable
from flask import jsonify, request


def _normalized_roles(raw_roles: str) -> set[str]:
    return {
        role.strip().lower()
        for role in (raw_roles or "").split(",")
        if role and role.strip()
    }


def enforce_api_access(allowed_roles: Iterable[str] | None = None):
    """
    Enforce role gate on protected routes.
    - `X-User-Role` must be in allowed_roles when provided.
    """
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
