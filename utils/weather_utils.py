import requests

def get_current_temperature(latitude: float, longitude: float) -> str | float:
    if latitude == "Not found" or longitude == "Not found":
        print("Invalid coordinates: skipping weather API.")
        return "Not available"

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current=temperature_2m"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("current", {}).get("temperature_2m", "Not available")
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return "Not available"
