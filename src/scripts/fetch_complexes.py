import requests
import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("API key not found")

URL = os.getenv("COMPLEXES_URL")
if not URL:
    raise ValueError("URL not found")

# Base directory = src/scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "complexes.json")

response = requests.get(URL, params={"api_key": API_KEY}, timeout=10)

if response.status_code == 200:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)
    print("Complexes data saved successfully at:", OUTPUT_PATH)
else:
    print("Failed to fetch complexes:", response.status_code)
