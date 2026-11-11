# Tennis Game Analytics

An interactive sports analytics project built with Python, SQLite, Streamlit, Pandas, and Plotly. It collects tennis competition, venue, and competitor-ranking data from the Sportradar Tennis API and presents selected metrics through a dashboard.

## Features

- Competition and category data collection
- Tennis complex and venue data collection
- Competitor ranking data collection
- SQLite storage for collected datasets
- Dashboard KPIs and competitor search
- Filters for rank, country, and points
- Leaderboards and country-level visualizations
- Interactive charts and geographic views using Plotly

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Requests
- Sportradar Tennis API

## Project Structure

The repository is organised into application, query, and script modules under `src/`. It also includes a `.env.example` file for configuration and a `requirements.txt` file for Python dependencies.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/manasvishetty327/tennis-game-analytics.git
cd tennis-game-analytics
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API

Copy `.env.example` to `.env` and configure the following values:

```env
SPORTRADAR_API_KEY=your_api_key
COMPETITIONS_URL=your_competitions_endpoint
COMPLEXES_URL=your_complexes_endpoint
RANKINGS_URL=your_rankings_endpoint
```

The collection scripts read these exact variable names. Keep `.env` private and do not commit API credentials.

Sportradar API access is subject to the account's plan, endpoint availability, and request limits.

## Data Collection

The repository contains separate scripts for collecting competition, complex/venue, and competitor-ranking data. Run the relevant scripts from the repository root, following their dependency order and the file paths present under `src/scripts/`.

The scripts create or populate SQLite databases used by the dashboard. Check the script configuration and database paths before running a collection task.

## Run the Dashboard

From the repository root:

```bash
streamlit run src/app/app.py
```

Streamlit displays the local dashboard URL in the terminal (usually http://localhost:8501).

## Notes

- The dashboard depends on the SQLite data being available at the paths expected by the application.
- API data collection requires a valid Sportradar API key and may be limited by the API plan.
- This is an analytics and visualization project; ranking and competition data should be interpreted in the context of the source API and its update schedule.

## Author

**Manasvi Shetty**
