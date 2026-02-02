"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset, DataLoader
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ====================
# SESSION STATE
# ====================
for key in ["region", "year_range"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ====================
# DATA LOADING
# ====================
download_dataset()
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

st.markdown("![neon](app/static/neonsign.png)")

st.title("Bellika's Retro: Retro Game Sales Dashboard")

# ====================
# MAIN DISPLAY
# ====================

# ======= Table placeholder =======

table_placeholder = st.empty()

# ============================
# CONTROLS
# ============================

# Toggle
on = st.toggle("Activate Nostalgia Age Filter")


# Age input
age_input = st.number_input("Insert age",min_value=17, max_value=60)
st.write("The current age is ", age_input)

age_range = nostalgia_age_filter(int(age_input))

# Select region
region = st.radio(
    "Select region to display sales",
    ("NA", "EU", "JP","OTHER","GLOBAL")
)

region_map = {
    "NA": "NA_Sales",
    "EU": "EU_Sales",
    "JP": "JP_Sales",
    "OTHER": "Other_Sales",
    "GLOBAL": "Global_Sales"
}
sales_col = region_map[region]

# Year slider ===========
years = sorted(df["Year"].dropna().unique())
selected_year = st.select_slider(
    "Release Year", 
    options=years,
    value=years[0]
    )

# =======================
# FILTER DATA
# =======================

filtered_df = filter_sales(df=df, region=sales_col, minimum=1.0)

if on:
    filtered_df = filtered_df[df["Year"].isin(age_range)]
else:
    filtered_df = filtered_df[df["Year"] == selected_year]


# =======================
# UPDATE TABLE PLACEHOLDER
# =======================

table_placeholder.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]].sort_values(
        by=sales_col, ascending=False
    ), hide_index=True
)

# Placeholder for map (could later use plotly or pydeck)
st.header(f"Interactive Sales Map ({st.session_state.region})")
st.write("Map feature coming here... for now just a placeholder")

# ====================
# FUTURE FEATURES
# ====================
st.write("Additional features can be added here: charts, graphs, or interactive maps.")
