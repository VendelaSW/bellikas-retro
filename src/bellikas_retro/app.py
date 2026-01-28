"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset
import streamlit as st
import pandas as pd
import numpy as np


download_dataset()
# ====================
# SESSION STATE
# ====================
for key in ["region", "year_range"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ====================
# DATA LOADING
# ====================
@st.cache_data
def load_data():
    # Placeholder for real CSV load
    # df = pd.read_csv("video_game_sales.csv")
    # For now, generate a dummy dataframe
    years = list(range(1980, 2021))  # 41 items

    data = {
        "Rank": range(1, 42),  # 41 items
        "Name": [f"Game {i}" for i in range(1, 42)],  # 41 items
        "Platform": (["PC", "PS4", "Xbox"] * 14)[:41],  # multiply enough then slice exactly 41
        "Year": years,
        "Genre": (["Action", "Adventure", "RPG", "Sports", "Puzzle"] * 9)[:41],  # 41 items
        "Publisher": (["Publisher A", "Publisher B", "Publisher C"] * 14)[:41],  # 41 items
        "NA_Sales": np.random.rand(41),
        "EU_Sales": np.random.rand(41),
        "JP_Sales": np.random.rand(41),
        "Other_Sales": np.random.rand(41),
        "Global_Sales": np.random.rand(41),
    }

    return pd.DataFrame(data)

df = load_data()

# ====================
# LAYOUT
# ====================
st.title("Bellika's Retro: Retro Game Sales Dashboard")

# Sidebar controls
st.sidebar.header("Filters")

# Slider for year range
year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
st.session_state.year_range = st.sidebar.slider(
    "Select release year range",
    year_min, year_max, (year_min, year_max)
)

# Select region
st.session_state.region = st.sidebar.radio(
    "Select region to display sales",
    ("NA", "EU", "JP")
)

# ====================
# FILTER DATA
# ====================
filtered_df = df[
    (df["Year"] >= st.session_state.year_range[0]) &
    (df["Year"] <= st.session_state.year_range[1])
]

# Map region selection to sales column
region_map = {
    "NA": "NA_Sales",
    "EU": "EU_Sales",
    "JP": "JP_Sales"
}
sales_col = region_map[st.session_state.region]

# ====================
# MAIN DISPLAY
# ====================
st.header(f"Top Games by {st.session_state.region} Sales")

st.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]].sort_values(
        by=sales_col, ascending=False
    )
)

# Placeholder for map (could later use plotly or pydeck)
st.header(f"Interactive Sales Map ({st.session_state.region})")
st.write("Map feature coming here... for now just a placeholder")

# ====================
# FUTURE FEATURES
# ====================
st.write("Additional features can be added here: charts, graphs, or interactive maps.")
