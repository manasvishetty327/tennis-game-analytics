import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px
import base64

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Tennis Game Analytics", layout="wide")

# ================= UI STYLES =================
st.markdown("""
<style>
.block-container {
    background: rgba(0, 0, 0, 0.30);
    padding: 2rem;
    border-radius: 18px;
}
.section-box {
    background: rgba(17, 24, 39, 0.88);
    padding: 26px;
    border-radius: 18px;
    margin-bottom: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    border-left: 6px solid #ff9800;
}
.section-title {
    font-size: 26px;
    font-weight: 600;
    color: #ffcc80;
    margin-bottom: 18px;
}
.kpi-card {
    background: linear-gradient(135deg, #ff9800, #ff5722);
    padding: 26px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
}
[data-testid="stDataFrame"] {
    background: rgba(0,0,0,0.85);
    border-radius: 12px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1f2937);
}
.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffcc80;
}
.sidebar-subtitle {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================= BACKGROUND IMAGE =================
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("src/app/assets/bg.jpg")

# ================= DATABASE (CORRECT ONE) =================
# app.py -> src/app/app.py
# DB -> src/scripts/competition.db
BASE_DIR = Path(__file__).resolve().parents[1]
MAIN_DB = BASE_DIR / "scripts" / "competition.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(MAIN_DB, check_same_thread=False)

# ================= LOAD DATA =================
def load_rank_data():
    query = """
    SELECT r.rank, r.movement, r.points, r.competitions_played,
           c.name, c.country
    FROM competitor_rankings r
    JOIN competitors c
    ON r.competitor_id = c.competitor_id
    """
    return pd.read_sql(query, get_connection())

def load_complex_data():
    return pd.read_sql(
        "SELECT complex_id, complex_name, country, timezone FROM complexes",
        get_connection()
    )

def load_venue_data():
    return pd.read_sql("""
        SELECT v.venue_id, v.venue_name,
               c.complex_name, c.country, c.timezone
        FROM venues v
        JOIN complexes c
        ON v.complex_id = c.complex_id
    """, get_connection())

df = load_rank_data()
complex_df = load_complex_data()
venue_df = load_venue_data()

# ================= SIDEBAR =================
st.sidebar.markdown("<div class='sidebar-title'>Tennis Game Analytics</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-subtitle'>Sports Data Analytics Dashboard</div>", unsafe_allow_html=True)

section = st.sidebar.radio("Navigation Menu", [
    "Dashboard",
    "Competitor Explorer",
    "Country Analysis",
    "Leaderboards",
    "Infrastructure Analysis",
    "About"
])

# ================= KPI CARD =================
def kpi_card(title, value):
    st.markdown(f"""
        <div class="kpi-card">
            <h2>{value}</h2>
            <p>{title}</p>
        </div>
    """, unsafe_allow_html=True)

# ================= DASHBOARD =================
if section == "Dashboard":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tennis Game Analytics Dashboard</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total Competitors", df.shape[0])
    with c2: kpi_card("Countries Represented", df["country"].nunique())
    with c3: kpi_card("Highest Points", int(df["points"].max()))

    country_df = df["country"].value_counts().reset_index()
    country_df.columns = ["Country", "Competitors"]

    st.plotly_chart(px.bar(country_df.head(15),
                           x="Country", y="Competitors",
                           color="Competitors",
                           template="plotly_dark"), use_container_width=True)

    st.plotly_chart(px.pie(country_df.head(8),
                           names="Country",
                           values="Competitors",
                           hole=0.5,
                           template="plotly_dark"), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= COMPETITOR EXPLORER =================
elif section == "Competitor Explorer":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Competitor Explorer</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rank_range = st.slider("Rank Range", 1, int(df["rank"].max()), (1, 50))
    with col2:
        countries = st.multiselect("Country", sorted(df["country"].unique()))
    with col3:
        min_points = st.slider("Minimum Points",
                               int(df["points"].min()),
                               int(df["points"].max()),
                               int(df["points"].min()))
    with col4:
        search = st.text_input("Search Competitor")

    filtered = df[
        df["rank"].between(rank_range[0], rank_range[1]) &
        (df["points"] >= min_points)
    ]

    if countries:
        filtered = filtered[filtered["country"].isin(countries)]
    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False)]

    st.dataframe(filtered.sort_values("rank"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= COUNTRY ANALYSIS =================
elif section == "Country Analysis":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Country-wise Analysis</div>', unsafe_allow_html=True)

    stats = df.groupby("country").agg(
        Total_Competitors=("name", "count"),
        Average_Points=("points", "mean")
    ).reset_index()

    st.plotly_chart(px.bar(stats.sort_values("Total_Competitors", ascending=False).head(15),
                           x="country", y="Total_Competitors",
                           template="plotly_dark"), use_container_width=True)

    st.plotly_chart(px.scatter(stats,
                               x="Total_Competitors",
                               y="Average_Points",
                               size="Average_Points",
                               color="country",
                               template="plotly_dark"), use_container_width=True)

    st.plotly_chart(px.choropleth(stats,
                                  locations="country",
                                  locationmode="country names",
                                  color="Total_Competitors",
                                  color_continuous_scale="Oranges",
                                  title="Global Tennis Competitor Distribution"),
                     use_container_width=True)

    st.dataframe(stats, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= LEADERBOARDS =================
elif section == "Leaderboards":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Leaderboards</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Top Ranked", "Highest Points"])
    with tab1:
        st.dataframe(df.sort_values("rank").head(10), use_container_width=True)
    with tab2:
        st.dataframe(df.sort_values("points", ascending=False).head(10), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= INFRASTRUCTURE (PERSON 2) =================
elif section == "Infrastructure Analysis":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Infrastructure & Venue Analysis</div>', unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1: kpi_card("Total Complexes", complex_df.shape[0])
    with k2: kpi_card("Total Venues", venue_df.shape[0])
    with k3: kpi_card("Countries with Venues", venue_df["country"].nunique())

    venues_per_complex = venue_df.groupby("complex_name").size().reset_index(name="Venues")

    st.plotly_chart(px.bar(venues_per_complex.sort_values("Venues", ascending=False).head(15),
                           x="complex_name", y="Venues",
                           template="plotly_dark"), use_container_width=True)

    country_venues = venue_df.groupby("country").size().reset_index(name="Venues")

    st.plotly_chart(px.pie(country_venues,
                           names="country",
                           values="Venues",
                           hole=0.45,
                           template="plotly_dark"), use_container_width=True)

    st.plotly_chart(px.choropleth(country_venues,
                                  locations="country",
                                  locationmode="country names",
                                  color="Venues",
                                  color_continuous_scale="Oranges",
                                  title="Global Tennis Infrastructure"),
                     use_container_width=True)

    st.dataframe(venue_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ABOUT =================
elif section == "About":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tennis Game</div>', unsafe_allow_html=True)
    st.markdown("Tennis is one of the most popular and widely played sports in the world, known for its combination of physical endurance, technical precision, strategic thinking, and mental resilience. It is played by individuals of all ages and skill levels, from recreational players to professional athletes competing on international stages. Tennis can be played in two primary formats: singles, where two players compete against each other, and doubles, where two teams of two players each face off. The objective of the game is to score points by hitting the ball over the net into the opponent’s court in such a way that the opponent cannot return it successfully within the rules. The origins of modern tennis can be traced back to Europe, particularly France and England, where earlier forms of the game were played as early as the twelfth century. Over time, tennis evolved into its current form during the late nineteenth century, with standardized rules, equipment, and court dimensions. The establishment of governing bodies helped regulate the sport globally, ensuring uniform rules, fair play, and structured competition. Today, tennis is governed internationally by professional organizations that oversee tournaments, player rankings, and rule enforcement.Tennis is played on different types of court surfaces, each of which significantly influences gameplay and player strategy. The three primary surfaces are grass, clay, and hard courts. Grass courts are fast-paced and favor players with strong serves and quick reflexes. Clay courts slow down the ball and produce higher bounces, encouraging longer rallies and emphasizing endurance and consistency. Hard courts offer a balanced playing environment, combining elements of speed and bounce that suit a wide range of playing styles. These surface variations make tennis a complex and dynamic sport, where adaptability plays a key role in success. Professional tennis follows a structured tournament system that allows players to compete at various levels throughout the year. Players earn ranking points based on their performance in tournaments, and these points determine their global rankings. Rankings are a critical aspect of professional tennis, as they influence tournament entry, seedings, and qualification for major events. Rankings are not static; they change frequently depending on match outcomes, points earned, and the number of tournaments played. This dynamic nature makes ranking analysis an important area of study in tennis analytics. Tennis tournaments are hosted across the world in a wide range of venues and sports complexes. These complexes often include multiple courts, training facilities, and supporting infrastructure to accommodate players, officials, and spectators. The geographical distribution of tennis venues reflects the global reach of the sport, with strong participation from Europe, the Americas, Asia, and other regions. Understanding the relationship between infrastructure, player representation, and competitive performance provides valuable insights into how tennis develops at national and international levels. In recent years, data analytics has become increasingly important in the sport of tennis. Large volumes of data are generated from matches, rankings, player movements, and tournament participation. This data can be analyzed to evaluate player performance, identify trends, compare competitors, and assess country-wise participation. Coaches, analysts, and sports organizations rely on data-driven insights to make informed decisions related to training, strategy, and player development. Tennis analytics enables the transformation of raw data into meaningful information through structured databases and visualizations. By organizing tennis data into relational databases and applying analytical queries, patterns and trends that are not immediately visible can be uncovered. Interactive dashboards further enhance understanding by allowing users to explore data through filters, charts, and geographic visualizations. These tools make complex tennis data more accessible to analysts, students, and enthusiasts alike. Overall, tennis is not only a sport of athletic excellence but also a domain rich in structured and unstructured data. The integration of tennis data with modern analytics platforms highlights the growing role of technology in sports. Tennis Game Analytics demonstrates how databases, programming, and visualization techniques can be combined to analyze sports data effectively. Through competitor analysis, country-wise insights, leaderboards, and infrastructure exploration, the platform showcases the practical application of data analytics concepts in the context of a globally recognized sport.")
    st.markdown("</div>", unsafe_allow_html=True)
