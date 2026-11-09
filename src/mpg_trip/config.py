import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

PORT = 8000

MAP_DIR = os.path.join(os.path.dirname(__file__), "..", "map")

ORS_API_KEY = os.getenv("ORS_API_KEY")

GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

FUEL_ECONOMY_BASE = "https://www.fueleconomy.gov/ws/rest/vehicle"

MENU_YEAR_URL = f"{FUEL_ECONOMY_BASE}/menu/year"
MENU_MAKE_URL = f"{FUEL_ECONOMY_BASE}/menu/make"
MENU_MODEL_URL = f"{FUEL_ECONOMY_BASE}/menu/model"
MENU_OPTIONS_URL = f"{FUEL_ECONOMY_BASE}/menu/options"
VEHICLE_URL = FUEL_ECONOMY_BASE