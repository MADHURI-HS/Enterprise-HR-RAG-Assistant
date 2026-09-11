import os


def login(username, password):
    """Validate credentials from environment variables.

    Set HR_USERNAME/HR_PASSWORD or ADMIN_USERNAME/ADMIN_PASSWORD before running.
    """
    users = {
        os.getenv("HR_USERNAME", ""): os.getenv("HR_PASSWORD", ""),
        os.getenv("ADMIN_USERNAME", ""): os.getenv("ADMIN_PASSWORD", ""),
    }
    return bool(username) and users.get(username) == password
