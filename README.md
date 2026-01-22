# Tennis Game Analytics
An interactive sports analytics dashboard built using Python, SQLite, Streamlit, Pandas, and Plotly.


## Main Folder Structure
```sportsGameAnalysis/
├── src/
│   ├── app/      streamlit application
│   ├── queries/  sql queries
│   ├── scripts/  python scripts/codes
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Competition Module 

This module extracts competition data from the SportRadar Tennis API.

### API Endpoint
https://api.sportradar.com/tennis/trial/v3/en/competitions.json

### Steps to Run
1. Add API key to `.env`
2. Run:
   python insert_data.py

### Output
- SQLite database: competition.db
- Tables: categories, competitions

### Folder Structure
```competition_module/
├── src/
│   ├── app/              streamlit application
│   ├── queries/
│   │  └── db_schema.sql  sql queries
│   ├── scripts/
│   │  ├── fetch_competitions.py
│   │  ├── parse_competitions.py
│   │  └── insert_data.py  
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Complexes & Venues Module 
This module handles tennis infrastructure data including complexes and venues.

- API Endpoint
https://api.sportradar.com/tennis/trial/v3/en/complexes.json

## Steps to Run
Add API key to .env

## Run:

python src/scripts/create_complex_tables.py
python src/scripts/fetch_complexes.py
python src/scripts/insert_complexes_venues.py



## Competitor Rankings & Analytics Module 
This module extracts ranking data from the SportRadar Tennis API and analysis it with SQL queries.

### API Endpoint
https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json

### Steps to Run
1. Add API key to `.env`
2. Run:
   python fetch_competitions.py
   python parse_competitions.py
   python insert_data.py

## Output
SQLite database: competition.db
Tables: complexes, venues

### Folder Structure
```complexes_venues_module/
src/
├── scripts/
│   ├── create_complex_tables.py
│   ├── fetch_complexes.py
│   ├── insert_complexes_venues.py
│   └── complexes.json
```

### Output
- SQLite database: rankings.db
- Tables: competitors, competitors_rankings

### Folder Structure
```competition_module/
├── src/
│   ├── app/              streamlit application
│   ├── queries/
│   │  └── db_schema.sql  sql queries
│   ├── scripts/
│   │  ├── fetch_rankings.py
│   │  ├── parse_rankings.py
│   │  └── insert_rankings.py  
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```


## Streamlit Application & Dashboard Module 

This module integrates all datasets from the SQLite database and displays them through an interactive Streamlit dashboard.

## Features

- KPI Dashboard (total competitors, countries, highest points)
- Competitor search and filters (rank, country, points)
- Leaderboards (top ranked, highest points)
- Country-wise analysis with charts and geo map
- Infrastructure analysis (complexes & venues)
- Interactive visualizations using Plotly
- Modern dark-themed UI with cards and sidebar navigation

## Technologies Used

1. Streamlit
2. Pandas
3. Plotly
4. SQLite
5. Python

### Folder Structure
```streamlit_module
├── src/
│   ├── app/
│   │   ├── app.py              streamlit main file
│   │   └── assets/
│   │       └── bg.jpg          background image
│   ├── scripts/
│   │   └── competition.db
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run

- streamlit run src/app/app.py

## Output

An interactive web dashboard for analyzing professional tennis data.
