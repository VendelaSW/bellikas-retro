import streamlit as st
import pandas as pd
import plotly.express as px

from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
from bellikas_retro.utils.config import REGION_COLUMN_MAP, REGION_RADIO_LABEL, REGIONS, TOGGLE_SALES_LABEL, MAX_AGE, MIN_AGE, AGE_INPUT_LABEL

init_session_state()
df = load_data()

st.title("Charts")

# =======================
# CONTROLS
# =======================
col1, col2 = st.columns(2)
with col1:
    sales_on = st.toggle(TOGGLE_SALES_LABEL)
with col2:
    region = st.radio(REGION_RADIO_LABEL, REGIONS)

sales_col = REGION_COLUMN_MAP[region]
st.session_state.region = region

age_input = st.number_input(
    AGE_INPUT_LABEL, 
    min_value=MIN_AGE, 
    max_value=MAX_AGE, 
    value=25, 
    key="charts_age"
)
age_range = nostalgia_age_filter(int(age_input))

filtered_df = df[df["Year"].isin(age_range)].copy()

# =======================
# FILTER DATA
# =======================
if sales_on and not filtered_df.empty:
    max_sales = float(filtered_df[sales_col].max() or 0.0)

    min_sales = st.slider(
        "Minimum sales (millions)",
        min_value=0.0,
        max_value=max(1.0, round(max_sales, 1)),
        value=1.0,
        step=0.1,
        format="%.1f",
        key="charts_min_sales"
    )

    filtered_df = filter_sales(
        df=filtered_df,
        region=sales_col,
        minimum=min_sales,
    )

# =======================
# TABLE
# =======================

if filtered_df.empty:
    st.info("No data matches the current filters.")
    st.stop()

# =======================
# CHART 1: SALES BY YEAR (REGION-AWARE)
# =======================
st.subheader(f"Sales by Year ({region})")

sales_by_year = (
    filtered_df
    .dropna(subset=["Year"])
    .groupby("Year", as_index=False)[sales_col]
    .sum()
    .sort_values("Year")
)

fig_year = px.line(
    sales_by_year,
    x="Year",
    y=sales_col,
    markers=True,
    title=f"{region} Sales by Year",
)

st.plotly_chart(fig_year, width='stretch')

# =======================
# CHART 2: PLATFORM x GENRE (MATCH REGION INSTEAD OF GLOBAL)
# =======================
st.subheader(f"{region} Sales by Platform and Genre")

platform_genre_sales = (
    filtered_df
    .groupby(["Platform", "Genre"])[sales_col]
    .sum()
    .reset_index()
)

fig_pg = px.bar(
    platform_genre_sales,
    x="Platform",
    y=sales_col,
    color="Genre",
    title=f"{region} Sales by Platform and Genre",
)

st.plotly_chart(fig_pg, width='stretch')

# =======================
# CHART 3: TOP 10 (MATCH REGION INSTEAD OF GLOBAL)
# =======================
st.subheader(f"Top 10 Best-Selling Games ({region})")

top_10 = (
    filtered_df
    .sort_values(sales_col, ascending=False)
    .head(10)
    .sort_values(sales_col)
)

fig_top10 = px.bar(
    top_10,
    y="Name",
    x=sales_col,
    orientation="h",
    title=f"Top 10 Best-Selling Games ({region})",
    text=sales_col,
)

st.plotly_chart(fig_top10, width='stretch')
