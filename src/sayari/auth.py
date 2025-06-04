import os
import requests

SAYARI_TOKEN_URL = "https://api.sayari.com/oauth/token"
CLIENT_ID = os.getenv("SAYARI_CLIENT_ID")
CLIENT_SECRET = os.getenv("SAYARI_CLIENT_SECRET")
AUDIENCE = "sayari.com"

def get_access_token():
    """Retrieve an access token from Sayari API using client credentials."""

    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Missing API credentials. Please set SAYARI_CLIENT_ID and SAYARI_CLIENT_SECRET environment variables.")

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(SAYARI_TOKEN_URL, json=payload)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("Token not found in Sayari response.")
        return token
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving token from Sayari API: {e}")
        raise
