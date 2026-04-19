import os
import requests
import streamlit as st


def get_api_base_url():
    return os.getenv("API_BASE_URL", "http://api:4000").rstrip("/")


def get_backend_role():
    role = st.session_state.get("role", "")
    role_map = {
        "student": "student",
        "professor": "professor",
        "data analyst": "analyst",
        "system admin": "admin",
        "analyst": "analyst",
        "admin": "admin",
    }
    return role_map.get(role, role)


def build_headers():
    headers = {
        "Content-Type": "application/json",
        "X-User-Role": get_backend_role(),
    }

    user_id = st.session_state.get("user_id")
    if user_id is not None:
        headers["X-User-Id"] = str(user_id)

    api_token = os.getenv("API_AUTH_TOKEN", "").strip()
    if api_token:
        headers["X-API-Token"] = api_token

    return headers


def _handle_response(response, default_message):
    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.ok:
        return data

    message = data.get("error", default_message)
    raise RuntimeError(message)


def api_get(path, params=None):
    response = requests.get(
        f"{get_api_base_url()}{path}",
        params=params,
        headers=build_headers(),
        timeout=10,
    )
    return _handle_response(response, "GET request failed.")


def api_post(path, payload=None):
    response = requests.post(
        f"{get_api_base_url()}{path}",
        json=payload,
        headers=build_headers(),
        timeout=10,
    )
    return _handle_response(response, "POST request failed.")


def api_put(path, payload=None):
    response = requests.put(
        f"{get_api_base_url()}{path}",
        json=payload,
        headers=build_headers(),
        timeout=10,
    )
    return _handle_response(response, "PUT request failed.")


def api_delete(path, payload=None):
    response = requests.delete(
        f"{get_api_base_url()}{path}",
        json=payload,
        headers=build_headers(),
        timeout=10,
    )
    return _handle_response(response, "DELETE request failed.")


def show_api_error(exc):
    st.error(str(exc))