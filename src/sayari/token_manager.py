from sayari.auth import get_access_token

# Cache token to avoid repeated requests
_cached_token = None

def get_token():
    global _cached_token
    if _cached_token is None:
        _cached_token = get_access_token()
    return _cached_token
