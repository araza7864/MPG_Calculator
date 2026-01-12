import os
import requests
ORS_api_key = os.getenv("ORS_API_KEY")
GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

def get_coordinates(address):
    params = {"api_key": ORS_api_key, "text": address, "size": 1}
    r = requests.get(GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data.get("features"):
        raise ValueError(f"Address not found: {address}")
    lon, lat = data["features"][0]["geometry"]["coordinates"]
    
    return lon, lat

def get_directions(start_lon, start_lat, end_lon, end_lat):
    params = {
        "api_key": ORS_api_key,
        "start": f"{start_lon},{start_lat}",
        "end": f"{end_lon},{end_lat}"
    }
    r = requests.get(DIRECTIONS_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    summary = data["features"][0]["properties"]["summary"]
    distance_meters = summary["distance"]
    duration_seconds = summary["duration"]
    return distance_meters, duration_seconds

str_address = input("What is your location: ")
end_address = input("Where would you like to go: ")
start_lon, start_lat = get_coordinates(str_address)
end_lon, end_lat = get_coordinates(end_address)

distance_meters, duration_seconds = get_directions(start_lon, start_lat, end_lon, end_lat)

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

def estimated_mpg(highway_weight):
    city_mpg = float(input("Enter your vehicle's city MPG: "))
    highway_mpg = float(input("Enter your vehicle's highway MPG: "))
    est_mpg = 1 / ((1 - highway_weight) / city_mpg + highway_weight / highway_mpg)
    return est_mpg
highway_weight_value = highway_weight(avg_speed)
estimated_mpg = estimated_mpg(highway_weight_value)

print(f"Distance: {distance_miles:.2f} miles")
print(f"Duration: {duration_seconds/60:.1f} minutes")
print(f"Avg speed: {avg_speed:.1f} mph")
print(f"Highway weight used: {highway_weight_value:.2f}")
print(f"Estimated MPG for your trip: {estimated_mpg:.2f} MPG")



