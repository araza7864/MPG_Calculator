import json
from pathlib import Path
from config import MAP_DIR, ORS_API_KEY
from route_service import get_coordinates, get_directions
from vehicle_service import get_vehicle_mpg
from mpg_calculator import highway_weight, estimated_mpg
from server import launch


def main():
    if not ORS_API_KEY:
        raise ValueError("Set ORS_API_KEY in the repository's .env file, or use --demo.")
    start_address = input("What is your location: ")
    end_address = input("Where would you like to go: ")

    start_lon, start_lat, start_label = get_coordinates(start_address)
    end_lon, end_lat, end_label = get_coordinates(end_address)

    distance_meters, duration_seconds, geojson_data = get_directions(
        start_lon, start_lat, end_lon, end_lat
    )

    distance_miles = distance_meters * 0.000621371
    if duration_seconds <= 0 or distance_meters <= 0:
        raise ValueError("Choose two different addresses with a non-zero driving route.")
    duration_hours = duration_seconds / 3600
    avg_speed = distance_miles / duration_hours

    city_mpg, highway_mpg = get_vehicle_mpg()

    weight = highway_weight(avg_speed)
    est_mpg = estimated_mpg(weight, city_mpg, highway_mpg)

    print(f"\nDistance: {distance_miles:.2f} miles")
    print(f"Duration: {duration_seconds/60:.1f} minutes")
    print(f"Avg speed: {avg_speed:.1f} mph")
    print(f"Estimated MPG: {est_mpg:.2f}")

    output = {
        "origin": start_label,
        "destination": end_label,
        "summary": {
            "distance_miles": distance_miles,
            "duration_minutes": duration_seconds / 60,
            "avg_speed_mph": avg_speed,
            "highway_weight": weight,
            "estimated_mpg": est_mpg,
        },
        "geojson": geojson_data
    }

    with (Path(MAP_DIR) / "route.json").open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("Route saved to map/route.json")


def demo():
    """Write a clearly labeled synthetic trip for a no-key local demonstration."""
    output = {
        "demo": True,
        "origin": "Demo starting point",
        "destination": "Demo destination",
        "summary": {
            "distance_miles": 12.0,
            "duration_minutes": 24.0,
            "avg_speed_mph": 30.0,
            "highway_weight": 0.4,
            "estimated_mpg": estimated_mpg(0.4, 24, 34),
        },
        "geojson": {
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "properties": {}, "geometry": {
                "type": "LineString",
                "coordinates": [[-77.32, 38.85], [-77.31, 38.84], [-77.30, 38.83]],
            }}],
        },
    }
    with (Path(MAP_DIR) / "route.json").open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)
    print("Synthetic demo saved. Distances and road geometry are illustrative, not a real route.")


if __name__ == "__main__":
    import argparse
    import requests
    parser = argparse.ArgumentParser(description="Estimate trip MPG and display a local route map")
    parser.add_argument("--demo", action="store_true", help="Use a synthetic example without API keys")
    parser.add_argument("--no-browser", action="store_true", help="Write JSON without starting the map server")
    args = parser.parse_args()
    try:
        demo() if args.demo else main()
    except ValueError as error:
        parser.exit(1, f"{error}\n")
    except requests.RequestException:
        parser.exit(1, "A route or vehicle API request failed. Check internet access, API configuration, and service availability.\n")
    if not args.no_browser:
        launch()
