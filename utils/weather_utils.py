import requests

def get_current_temperature(latitude: float, longitude: float) -> float | str:
    if latitude == "Not found" or longitude == "Not found":
        print("Skipping weather lookup — no coordinates available.")
        return "Not available"

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current=temperature_2m"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature = data.get("current", {}).get("temperature_2m")
        return temperature if temperature is not None else "Not available"

    except requests.RequestException as e:
        print(f"Couldn’t get weather info: {e}")
        return "Not available"
