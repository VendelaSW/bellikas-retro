"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset, DataLoader
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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

controls_container = st.container()
controls_container.empty()
# ====== Sales per year chart ======

chart_container = st.container()
chart_container.empty()


# ====== Genre/Platform comparison chart ======

bar_ch_container = st.container()
bar_ch_container.empty()

# ====== Top 10 chart ======

hbar_ch_container = st.container()
hbar_ch_container.empty()

# ======= Table placeholder =======

table_placeholder = st.empty()

# ============================
# CONTROLS
# ============================
with controls_container:
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

# Genre/Platform comparison filter
platform_genre_sales = (
    filtered_df
    .groupby(["Platform", "Genre"])["Global_Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    platform_genre_sales,
    x="Platform",
    y="Global_Sales",
    color="Genre",
    title="Global Sales by Platform and Genre",
)

# Top 10 filter
top_10 = (
    filtered_df.sort_values("Global_Sales", ascending=False)
    .head(10)
    .sort_values("Global_Sales")
)

ax = px.bar(
    top_10,
    y="Name",
    x="Global_Sales",
    orientation="h",
    title="Top 10 Best-Selling Games (Global)",
    color="Global_Sales",
    text="Global_Sales"
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

with bar_ch_container:
    st.plotly_chart(fig, width='stretch')

with hbar_ch_container:
    st.plotly_chart(ax, width="stretch")