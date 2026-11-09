# Smart Trip MPG Calculator

A Python command-line app that combines a driving route with vehicle fuel-economy data to estimate trip MPG. The result includes a local Leaflet map and a JSON route summary.

## What it does

- Geocodes two addresses and retrieves a driving route through OpenRouteService.
- Lets you select a vehicle using FuelEconomy.gov data.
- Estimates city/highway driving mix from the route's average speed and combines the vehicle's city/highway MPG using a weighted harmonic mean.
- Displays distance, duration, estimated MPG, and the route on an interactive map.

These are heuristic estimates, not measured fuel consumption. The current CLI calculates one route per run; it does not automatically compare alternate routes or account for traffic, weather, elevation, or driving style.

## Run locally

Requires Python 3.12+, an OpenRouteService API key, and internet access.

```bash
git clone https://github.com/araza7864/MPG_Calculator.git
cd MPG_Calculator
python -m venv .venv
```

Activate with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on macOS/Linux, then:

```bash
python -m pip install -r requirements.txt
```

For a quick demonstration without API keys:

```bash
python src/mpg_trip/main.py --demo
```

The demo is explicitly labeled synthetic. It exercises JSON output and the map display; map tiles and Leaflet still need internet access. Add `--no-browser` to generate the JSON without starting a server.

Copy `.env.example` to `.env` in the repository root and set `ORS_API_KEY`. Then run from the repository root:

```bash
python src/mpg_trip/main.py
```

Follow the address and vehicle prompts. The app saves `src/map/route.json` and opens `http://localhost:8000/map.html`. Keep the terminal running while viewing the map; press Ctrl+C to stop. Local route output and API keys are ignored by Git.

## Project layout

- `src/mpg_trip/`: routing, vehicle lookup, fuel model, CLI, and local map server.
- `src/map/map.html`: Leaflet route display.
- `.env.example`: configuration template containing no credentials.

## Checks

```bash
python -m unittest discover -s tests
```

The checks run without API keys or network calls. A full trip requires live API access.
