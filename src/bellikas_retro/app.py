"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset, DataLoader
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path




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
    loader = DataLoader(data_dir=Path("data"))

    df = loader.load()
    return pd.DataFrame(df)

df = load_data()

# ====================
# LAYOUT
# ====================
st.title("Bellika's Retro: Retro Game Sales Dashboard")

# Display static image
st.markdown("![Kingen](app/static/kingen.jpeg)")

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
