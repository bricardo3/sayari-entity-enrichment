import os
import requests

SAYARI_TOKEN_URL = "https://api.sayari.com/oauth/token"
CLIENT_ID = os.getenv("SAYARI_CLIENT_ID")
CLIENT_SECRET = os.getenv("SAYARI_CLIENT_SECRET")
AUDIENCE = "sayari.com"

def get_access_token():
    # Faz a autenticação com a API da Sayari usando client credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("API credentials are missing. Please check SAYARI_CLIENT_ID and SAYARI_CLIENT_SECRET.")

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
            raise ValueError("Access token not found in the response.")
        return token
    except requests.exceptions.RequestException as e:
        print("Couldn’t retrieve token from Sayari API.")
        print(e)
        raise
