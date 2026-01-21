import os
import requests
import json
ORS_api_key = os.getenv("ORS_API_KEY")
GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
FUEL_ECONOMY_BASE = "https://www.fueleconomy.gov/ws/rest/vehicle"

MENU_YEAR_URL = f"{FUEL_ECONOMY_BASE}/menu/year"
MENU_MAKE_URL = f"{FUEL_ECONOMY_BASE}/menu/make"
MENU_MODEL_URL = f"{FUEL_ECONOMY_BASE}/menu/model"
MENU_OPTIONS_URL = f"{FUEL_ECONOMY_BASE}/menu/options"
VEHICLE_URL = f"{FUEL_ECONOMY_BASE}"
#look up vehicle profile for more accurate mpg estimate, possibly use Fueleconomy.gov API
#have to add 5 options for address accuracy

def get_coordinates(address):
    params = {"api_key": ORS_api_key, "text": address, "size": 1}
    r = requests.get(GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data.get("features"):
        raise ValueError(f"Address not found: {address}")
    lon, lat = data["features"][0]["geometry"]["coordinates"]
    label = data["features"][0]["properties"]["label"]
    
    return lon, lat, label

def get_directions(start_lon, start_lat, end_lon, end_lat):

    headers = {"Authorization": ORS_api_key, "Content-Type": "application/json"}
    body = {"coordinates": [[start_lon, start_lat], [end_lon, end_lat]]}

    r = requests.post(DIRECTIONS_URL, headers=headers, json=body, timeout=15)
    if not r.ok:
        print("ORS Directions status: ", r.status_code)
        print("ORS Directions response: ", r.text[:500])
        r.raise_for_status()
    geojson_data = r.json()

    summary = geojson_data["features"][0]["properties"]["summary"]
    distance_meters = summary["distance"]
    duration_seconds = summary["duration"]

    return distance_meters, duration_seconds, geojson_data

def fetch_menu_items(url, params=None):
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    print("FuelEconomy status:", r.status_code)
    print("FuelEconomy content-type:", r.headers.get("Content-Type"))
    print("FuelEconomy first 120 chars:", r.text[:120])
    r.raise_for_status()
    data = r.json()

    items = data.get("menuItem", [])
    return items

def choose_from_menu(items, prompt):
    print(prompt)
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['text']}")

    while True:
        choice = input("Pick a number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(items):
                return items[idx - 1]
        print("Invalid choice. Please try again.")

def get_vehicle_mpg():
    year_items = fetch_menu_items(MENU_YEAR_URL)
    year_choice = choose_from_menu(year_items, "Select vehicle year:")
    year = year_choice["value"]

    make_items = fetch_menu_items(MENU_MAKE_URL, params={"year": year})
    make_choice = choose_from_menu(make_items, "Select vehicle make:")
    make = make_choice["value"]

    model_items = fetch_menu_items(MENU_MODEL_URL, params={"year": year, "make": make})
    model_choice = choose_from_menu(model_items, "Select vehicle model:")
    model = model_choice["value"]

    option_items = fetch_menu_items(MENU_OPTIONS_URL, params={"year": year, "make": make, "model": model})
    option_choice = choose_from_menu(option_items, "Select vehicle option:")
    option = option_choice["value"]

    vehicle_params = {"year": year, "make": make, "model": model, "option": option}
    r = requests.get(VEHICLE_URL, params=vehicle_params, timeout=15)
    r.raise_for_status()
    data = r.json()

    city_mpg = float(data["city08"])
    highway_mpg = float(data["highway08"])

    return city_mpg, highway_mpg

str_address = input("What is your location: ")
end_address = input("Where would you like to go: ")
start_lon, start_lat, str_loc = get_coordinates(str_address)
end_lon, end_lat, end_add = get_coordinates(end_address)

distance_meters, duration_seconds, geojson_data = get_directions(start_lon, start_lat, end_lon, end_lat)

distance_miles = distance_meters * 0.000621371
duration_hours = duration_seconds / 3600
avg_speed = distance_miles / duration_hours

city_mpg_value, highway_mpg_value = get_vehicle_mpg()

def highway_weight(avg_speed):
    if avg_speed < 25:
        return 0.15
    elif avg_speed < 40:
        return 0.40
    elif avg_speed < 55:
        return 0.70
    else:
        return 0.85

def estimated_mpg(highway_weight, city_mpg, highway_mpg):
    est_mpg = 1 / ((1 - highway_weight) / city_mpg + highway_weight / highway_mpg)
    return est_mpg
highway_weight_value = highway_weight(avg_speed)
est_mpg = estimated_mpg(highway_weight_value, city_mpg_value, highway_mpg_value)

print(f"Distance: {distance_miles:.2f} miles")
print(f"Duration: {duration_seconds/60:.1f} minutes")
print(f"Avg speed: {avg_speed:.1f} mph")
print(f"Highway weight used: {highway_weight_value:.2f}")
print(f"Estimated MPG for your trip: {est_mpg:.2f} MPG")

output = {
    "origin": str_loc,
    "destination": end_add,
    "summary": {
    "distance_miles": distance_miles,
    "duration_minutes": duration_seconds/60,
    "avg_speed_mph": avg_speed,
    "highway_weight": highway_weight_value,
    "estimated_mpg": est_mpg,
    },
    "geojson": geojson_data
}
with open("../map/route.json", "w") as f:
    json.dump(output, f, indent = 2)

print("Route data saved to map/route.json")
