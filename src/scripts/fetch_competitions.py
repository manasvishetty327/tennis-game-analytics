import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("API key not found")

URL = os.getenv("COMPETITIONS_URL")
if not URL:
    raise ValueError("URL not found")

def fetch_competitions():
    response = requests.get(
        URL,
        params={"api_key": API_KEY},
        timeout=10
    )
    response.raise_for_status()
    return response.json()["competitions"]

if __name__ == "__main__":
    data = fetch_competitions()
    print("✅ API USED SUCCESSFULLY")
    print("Total competitions:", len(data))
    print("Sample record:", data[0])
