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
        data = response.json().get("data", [])

        if not data:
            print(f"Not found: {entry['name']} ({entry['country']})")
            return "Not found", "Not found", "Not found"

        # Sayari returns the most relevant result first
        first_result = data[0]
        entity_id = first_result.get("id", "Not found")
        print(f"Found entity_id: {entity_id}")

        coordinates = first_result.get("coordinates", [])
        lat = lng = "Not found"

        if coordinates and isinstance(coordinates, list) and len(coordinates) > 0:
            lat = coordinates[0].get("lat", "Not found")
            lng = coordinates[0].get("lng", "Not found")
            print(f"Coordinates found: ({lat}, {lng})")
        else:
            print("No coordinates found.")

        return entity_id, lat, lng

    except requests.exceptions.RequestException as e:
        print(f"Error searching entity: {entry['name']}, Reason: {str(e)}")
        return "Not found", "Not found", "Not found"
