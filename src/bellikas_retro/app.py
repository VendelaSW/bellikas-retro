"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset, DataLoader
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

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
    loader = DataLoader(data_dir=Path("data"))
    df = loader.load()
    return pd.DataFrame(df)

df = load_data()

# ====================
# LAYOUT
# ====================
st.set_page_config(layout="centered")
st.markdown("![neon](app/static/neonsign.png)")

# ====================
# MAIN DISPLAY
# ====================

# ====== Sales per year chart ======

chart_container = st.container()
chart_container.empty()


# ====== Genre/Platform comparison chart ======



# ====== Top 10 chart ======



# ======= Table placeholder =======

table_placeholder = st.empty()

# ============================
# CONTROLS
# ============================

col1, col2 = st.columns(2)

with col1:
    on = st.toggle("Activate Nostalgia Age Filter")
with col2:
    sales_on = st.toggle("Activate Min Sales Filter")

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

filtered_df = df.copy()

#  Optional filters
if on:
    filtered_df = filtered_df[filtered_df["Year"].isin(age_range)]
else:
    filtered_df = filtered_df[df["Year"] == selected_year]

if sales_on:
    filtered_df = filter_sales(
        df=filtered_df, 
        region=sales_col, 
        minimum=1.0
    )

# Sales by year filter
sales_by_year = (
    filtered_df
    .groupby("Year", as_index=False)[sales_col]
    .sum()
    .sort_values("Year")
)

# =======================
# UPDATE TABLE PLACEHOLDER
# =======================

table_placeholder.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]].sort_values(
        by=sales_col, ascending=False
    ), hide_index=True
)

# Sales by year chart update
with chart_container:
    st.subheader("Sales by Year")
    st.line_chart(
        data=sales_by_year,
        x="Year",
        y=sales_col
    )
