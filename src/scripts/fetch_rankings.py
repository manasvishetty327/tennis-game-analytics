import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("API key not found")

URL = os.getenv("RANKINGS_URL")
if not URL:
    raise ValueError("URL not found")


def fetch_rankings():
    try:
        response = requests.get(URL, params={"api_key": API_KEY}, timeout=10)
        response.raise_for_status()

        data = response.json()

        if isinstance(data.get("rankings"), list):
            return data["rankings"]

        return []

    except requests.exceptions.RequestException as e:
        print("API error:", e)
        return []
