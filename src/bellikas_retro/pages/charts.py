import streamlit as st
import pandas as pd
import plotly.express as px

from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import filter_sales
from bellikas_retro.utils.config import REGION_COLUMN_MAP, REGION_RADIO_LABEL, REGIONS, TOGGLE_SALES_LABEL

init_session_state()
df = load_data()

st.title("Charts", anchor='charts')

st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

#charts {
  margin-top: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 4rem;
  color: #ffd6eb;

  -webkit-text-stroke: 0.7px rgba(255, 230, 230, 0.55);
  -webkit-font-smoothing: antialiased;

  animation: flicker 3.0s infinite;

  text-shadow:
    0 0 1px rgba(255,255,255,0.35),
    0 0 3px rgba(255,180,220,0.35),
    0 0 8px rgba(230, 30, 150, 1),
    0 0 16px rgba(210, 10, 130, 0.95),
    0 0 28px rgba(180, 0, 110, 0.8),
    0 0 46px rgba(150, 0, 90, 0.7),
    0 0 70px rgba(120, 0, 70, 0.6);
}

@keyframes flicker {
  0%, 38%, 100% { opacity: 1; }
  40% { opacity: 0.9; }
  41% { opacity: 0.75; }
  42% { opacity: 1; }
  78% { opacity: 0.95; }
}
</style>

""",
unsafe_allow_html=True,
)

# =======================
# Controls
# =======================
col1, col2 = st.columns(2)
with col1:
    sales_on = st.toggle(TOGGLE_SALES_LABEL)
with col2:
    region = st.radio(REGION_RADIO_LABEL, REGIONS)

sales_col = REGION_COLUMN_MAP[region]
st.session_state.region = region


# =======================
# YEAR SLIDER (NO AGE FILTER)
# =======================
year_min = int(df["Year"].min())
year_max = int(df["Year"].max())

year_range = st.slider(
    "Select year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
    key="charts_year_range",
)

filtered_df = df[df["Year"].between(year_range[0], year_range[1])].copy()

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
# Handle Empty
# =======================

if filtered_df.empty:
    st.info("No data matches the current filters.")
    st.stop()

# =======================
# CHART 1: SALES BY YEAR (REGION)
# =======================
st.subheader(f"Sales by Year ({region})")

sales_by_year = (
    filtered_df
    .dropna(subset=["Year"])
    .groupby("Year")
    .agg(
        total_sales=(sales_col, "sum"),
        unique_games=("Name", "nunique"),
    )
    .reset_index()
)

sales_by_year["avg_sales_per_game"] = (
    sales_by_year["total_sales"] / sales_by_year["unique_games"]
)

fig_total = px.line(
    sales_by_year,
    x="Year",
    y="total_sales",
    markers=True,
    title=f"Total {region} Sales by Year",
)

st.plotly_chart(fig_total, width='stretch')

fig_avg = px.line(
    sales_by_year,
    x="Year",
    y="avg_sales_per_game",
    markers=True,
    title=f"Average {region} Sales per Game by Year",
)

st.plotly_chart(fig_avg, width='stretch')

# =======================
# CHART 2: PLATFORM x GENRE (REGION)
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
# CHART 3: TOP 10 (REGION)
# =======================
st.subheader(f"Top 10 Best-Selling Games ({region})")

by_name_platform = (
    filtered_df
    .groupby(["Name", "Platform"], as_index=False)[sales_col]
    .sum()
)

top_names = (
    by_name_platform
    .groupby("Name", as_index=False)[sales_col]
    .sum()
    .sort_values(sales_col, ascending=False)
    .head(10)["Name"]
)

top_10_platform = by_name_platform[by_name_platform["Name"].isin(top_names)]

fig_top10 = px.bar(
    top_10_platform,
    y="Name",
    x=sales_col,
    color="Platform",
    orientation="h",
    title=f"Top 10 Best-Selling Games ({region})",
)

fig_top10.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig_top10, width='stretch')
