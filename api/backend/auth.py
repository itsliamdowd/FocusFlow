from typing import Iterable
from flask import jsonify, request


def _normalized_roles(raw_roles: str) -> set[str]:
    return {
        role.strip().lower()
        for role in (raw_roles or "").split(",")
        if role and role.strip()
    }


def enforce_api_access(allowed_roles: Iterable[str] | None = None):
    """Auth disabled for local-only deployment."""
    return None


def enforce_user_scope(requested_user_id):
    """Auth disabled for local-only deployment."""
    return None
