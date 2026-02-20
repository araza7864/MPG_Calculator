import requests
from config import ORS_API_KEY, GEOCODE_URL, DIRECTIONS_URL


def get_coordinates(address):
    params = {"api_key": ORS_API_KEY, "text": address, "size": 1}
    r = requests.get(GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    features = data.get("features", [])
    if not features:
        raise ValueError(f"Address not found or ambiguous: {address}")

    lon, lat = features[0]["geometry"]["coordinates"]
    label = features[0]["properties"]["label"]

    return lon, lat, label


def get_directions(start_lon, start_lat, end_lon, end_lat):
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {"coordinates": [[start_lon, start_lat], [end_lon, end_lat]]}

    r = requests.post(DIRECTIONS_URL, headers=headers, json=body, timeout=15)
    r.raise_for_status()
    geojson_data = r.json()

    summary = geojson_data["features"][0]["properties"]["summary"]
    distance_meters = summary["distance"]
    duration_seconds = summary["duration"]

    return distance_meters, duration_seconds, geojson_data