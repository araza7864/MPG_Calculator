import requests
import math
from config import (
    MENU_YEAR_URL,
    MENU_MAKE_URL,
    MENU_MODEL_URL,
    MENU_OPTIONS_URL,
    VEHICLE_URL
)


def fetch_menu_items(url, params=None):
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    items = data.get("menuItem", [])

    if isinstance(items, dict):
        items = [items]

    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
        else:
            normalized.append({"text": item, "value": item})

    return normalized


def choose_from_menu(items, prompt, per_row=4):
    if len(items) == 1:
        print(f"{prompt} {items[0]['text']} (auto-selected)")
        return items[0]

    print(prompt)

    longest = max(len(f"{i+1}. {item['text']}") for i, item in enumerate(items))
    col_width = longest + 4
    rows = math.ceil(len(items) / per_row)

    for r in range(rows):
        for c in range(per_row):
            idx = r + c * rows
            if idx < len(items):
                text = f"{idx+1}. {items[idx]['text']}"
                print(f"{text:<{col_width}}", end="")
        print()

    while True:
        choice = input(f"Pick a number (1-{len(items)}): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(items):
                return items[idx - 1]
        print("Invalid choice. Please try again.")


def get_vehicle_mpg():
    year = choose_from_menu(fetch_menu_items(MENU_YEAR_URL), "Select vehicle year:")["value"]

    make = choose_from_menu(
        fetch_menu_items(MENU_MAKE_URL, {"year": year}),
        "Select vehicle make:"
    )["value"]

    model = choose_from_menu(
        fetch_menu_items(MENU_MODEL_URL, {"year": year, "make": make}),
        "Select vehicle model:"
    )["value"]

    vehicle_id = choose_from_menu(
        fetch_menu_items(MENU_OPTIONS_URL, {"year": year, "make": make, "model": model}),
        "Select vehicle option:"
    )["value"]

    r = requests.get(f"{VEHICLE_URL}/{vehicle_id}", headers={"Accept": "application/json"}, timeout=15)
    r.raise_for_status()
    data = r.json()

    return float(data["city08"]), float(data["highway08"])