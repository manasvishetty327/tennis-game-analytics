import sqlite3, os
from parse_rankings import parse_rankings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "competition.db")

def create_tables(cursor):
    cursor.executescript(
        """
    CREATE TABLE IF NOT EXISTS competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS competitor_rankings (
        rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50) NOT NULL,
        FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
    );
    """
    )

def insert_data():
    competitors, rankings = parse_rankings()
    print(f"Total competitors: {len(competitors)}, Total rankings: {len(rankings)}")

    # IMPORTANT: use DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    create_tables(cursor)

    # Insert competitors
    for comp in competitors.values():
        cursor.execute(
            """
            INSERT OR IGNORE INTO competitors
            (competitor_id, name, country, country_code, abbreviation)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                comp["competitor_id"],
                comp["name"],
                comp["country"],
                comp["country_code"],
                comp["abbreviation"],
            ),
        )

    # Insert rankings
    for r in rankings:
        cursor.execute(
            """
            INSERT OR IGNORE INTO competitor_rankings
            (rank, movement, points, competitions_played, competitor_id)
            SELECT ?, ?, ?, ?, ?
            WHERE EXISTS (
                SELECT 1 FROM competitors WHERE competitor_id = ?
            )
        """,
            (
                r["rank"],
                r["movement"],
                r["points"],
                r["competitions_played"],
                r["competitor_id"],
                r["competitor_id"],
            ),
        )

    conn.commit()
    conn.close()
    print("✅ Competitor rankings inserted into src/scripts/competition.db")

if __name__ == "__main__":
    insert_data()
