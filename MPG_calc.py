import requests
#need another api key for longitude and latitude from each address
API_KEY = ""

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
    ""