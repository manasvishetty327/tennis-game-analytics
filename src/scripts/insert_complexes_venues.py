import json
import sqlite3
import os

# Base directory = src/scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DB is also inside src/scripts
DB_PATH = os.path.join(BASE_DIR, "competition.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load complexes JSON (also in src/scripts)
with open(os.path.join(BASE_DIR, "complexes.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

for c in data.get("complexes", []):
    complex_id = c.get("id")
    complex_name = c.get("name")

    venues = c.get("venues", [])

    country = None
    timezone = None
    if venues:
        country = venues[0].get("country_name")
        timezone = venues[0].get("timezone")

    cursor.execute(
        """
        INSERT OR IGNORE INTO complexes
        (complex_id, complex_name, country, timezone)
        VALUES (?, ?, ?, ?)
        """,
        (complex_id, complex_name, country, timezone)
    )

    for v in venues:
        cursor.execute(
            """
            INSERT OR IGNORE INTO venues
            (venue_id, venue_name, complex_id)
            VALUES (?, ?, ?)
            """,
            (v.get("id"), v.get("name"), complex_id)
        )

conn.commit()
conn.close()

print("Complexes & venues inserted into src/scripts/competition.db")
