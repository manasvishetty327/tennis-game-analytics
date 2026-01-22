import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "competition.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS complexes (
    complex_id TEXT PRIMARY KEY,
    complex_name TEXT,
    country TEXT,
    timezone TEXT
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id TEXT PRIMARY KEY,
    venue_name TEXT,
    complex_id TEXT,
    FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
);
""")

conn.commit()
conn.close()
print("✅ complexes and venues tables created")
