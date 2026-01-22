-- Categorires and Competition Schema
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

-- Competitor and Competitor Rankings Schema
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id INT PRIMARY KEY AUTOINCREMENT,
    rank INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);

-- Complexes and Venues Schema
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
