import os
import requests
#need another api key for longitude and latitude from each address
ORS_api_key = os.getenv("ORS_API_KEY")
GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"

distance_miles = distance_meters * 0.000621371
duration_hours = duration_seconds / 3600
avg_speed = distance_miles / duration_hours

def highway_weight(avg_speed):
    if avg_speed < 25:
        return 0.15
    elif avg_speed < 40:
        return 0.40
    elif avg_speed < 55:
        return 0.70
    else:
        return 0.85
def get_coordinates(address):
    params = {"api key": ORS_api_key, "text": address, "size": 1}
    r = requests.get(GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data.get("features"):
        raise ValueError(f"Address not found: {address}")
    lon, lat = data["features"][0]["geometry"]["coordinates"]
    
    return lon, lat
def estimated_mpg(highway_weight):
    ""