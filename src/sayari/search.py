from typing import Any
import requests

SAYARI_SEARCH_URL = "https://api.sayari.com/v1/search/entity"

def search_entity_and_coordinates(entry: dict, token: str) -> tuple[Any, Any, Any] | tuple[str, str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    query = f"\"{entry['name']}\""

    payload = {
        "q": query,
        "fields": ["name"],
        "filter": {
            "entity_type": ["company"],
            "country": [entry["country"]]
        },
        "advanced": True,
        "facets": False
    }

    try:
        response = requests.post(SAYARI_SEARCH_URL, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json().get("data", [])

        if not results:
            print(f"No match for: {entry['name']} ({entry['country']})")
            return "Not found", "Not found", "Not found"

        top_result = results[0]
        entity_id = top_result.get("id", "Not found")

        coordinates = top_result.get("coordinates", [])
        lat = lng = "Not found"

        if coordinates and isinstance(coordinates, list) and len(coordinates) > 0:
            lat = coordinates[0].get("lat", "Not found")
            lng = coordinates[0].get("lng", "Not found")
        else:
            print(f"No coordinates found for: {entry['name']}")

        return entity_id, lat, lng

    except requests.exceptions.RequestException as e:
        print(f"Request error while searching for: {entry['name']} – {e}")
        return "Not found", "Not found", "Not found"
