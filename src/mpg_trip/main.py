import json
from route_service import get_coordinates, get_directions
from vehicle_service import get_vehicle_mpg
from mpg_calculator import highway_weight, estimated_mpg
from server import launch


def main():
    start_address = input("What is your location: ")
    end_address = input("Where would you like to go: ")

    start_lon, start_lat, start_label = get_coordinates(start_address)
    end_lon, end_lat, end_label = get_coordinates(end_address)

    distance_meters, duration_seconds, geojson_data = get_directions(
        start_lon, start_lat, end_lon, end_lat
    )

    distance_miles = distance_meters * 0.000621371
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

    with open("../map/route.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Route saved to map/route.json")


if __name__ == "__main__":
    main()
    launch()