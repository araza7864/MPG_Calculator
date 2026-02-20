# MPG Trip Estimator

A full-stack Python project that estimates real-world fuel efficiency for a trip by combining routing data, vehicle MPG statistics, and speed-based modeling.

The application calculates a route between two addresses, estimates average speed, applies a highway/city weighting algorithm, and visualizes the route on a local interactive map.

---

## Features

- Address geocoding using OpenRouteService API
- Route calculation with distance and duration analysis
- Vehicle selection via FuelEconomy.gov API
- Speed-based MPG estimation algorithm
- GeoJSON route visualization
- Local HTTP server for map rendering
- Modular Python architecture

---

## Tech Stack

- Python
- Requests
- HTTPServer
- REST APIs
- GeoJSON
- HTML/JavaScript map visualization

---

## Project Structure


src/
map/
map.html
route.json

mpg_trip/
main.py
config.py
route_service.py
vehicle_service.py
mpg_calculator.py
server.py


---

## Setup

### 1. Clone repository


git clone <repo-url>
cd MPG_Calculator


### 2. Install dependencies


pip install -r requirements.txt


### 3. Create environment variables

Copy `.env.example` to `.env`:


ORS_API_KEY=your_api_key_here


---

## Run


python main.py


The browser will automatically open the map interface.

---

## How It Works

1. User enters origin and destination.
2. OpenRouteService calculates route data.
3. FuelEconomy API retrieves vehicle MPG stats.
4. Estimated MPG is calculated using a speed-weighted model.
5. Route data is saved as GeoJSON and visualized locally.

---

## Future Improvements

- Convert to FastAPI backend
- Web UI for input instead of CLI
- Persistent history storage
- Deployment-ready version

---

## Author

Asad Raza   