import sqlite3, os
from parse_competitions import parse_competitions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "competition.db")

def create_tables(cursor):
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id TEXT PRIMARY KEY,
        category_name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS competitions (
        competition_id TEXT PRIMARY KEY,
        competition_name TEXT NOT NULL,
        parent_id TEXT,
        type TEXT,
        gender TEXT,
        category_id TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """)

def insert_data():
    categories, competitions = parse_competitions()

    # IMPORTANT: use DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_tables(cursor)

    for cat_id, cat_name in categories.items():
        cursor.execute(
            "INSERT OR IGNORE INTO categories VALUES (?, ?)",
            (cat_id, cat_name)
        )

    for comp in competitions:
        cursor.execute(
            """INSERT OR IGNORE INTO competitions
            (competition_id, competition_name, parent_id, type, gender, category_id)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                comp["competition_id"],
                comp["competition_name"],
                comp["parent_id"],
                comp["type"],
                comp["gender"],
                comp["category_id"]
            )
        )

    conn.commit()
    conn.close()
    print("✅ DATA INSERTED INTO src/scripts/competition.db")

if __name__ == "__main__":
    insert_data()
