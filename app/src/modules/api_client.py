import os


def get_api_base_url():
    """
    Resolve API base URL from environment with a safe default.
    """
    return os.getenv("API_BASE_URL", "http://localhost:4000").rstrip("/")
