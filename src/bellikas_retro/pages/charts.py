import streamlit as st
import pandas as pd
import plotly.express as px

from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import filter_sales
from bellikas_retro.utils.config import REGION_COLUMN_MAP, REGION_RADIO_LABEL, REGIONS, TOGGLE_SALES_LABEL
from bellikas_retro.utils.validations import get_sales_column, validate_min_sales, validate_years

init_session_state()
df = load_data()
if df.empty:
    st.warning("Dataset not available in this environment.")
    st.stop()

st.title("Charts", anchor='charts')

st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

#charts {
  margin-top: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 4rem;
  color: #ffeaf3;

  -webkit-text-stroke: 0.7px rgba(255, 230, 230, 0.55);
  -webkit-font-smoothing: antialiased;

  animation: flicker 3.0s infinite;

  text-shadow:
    0 0 1px rgba(255,255,255,0.7),
    0 0 4px rgba(255,230,245,0.6),
    0 0 6px rgba(235, 60, 170, 0.95),
    0 0 14px rgba(215, 30, 150, 0.9),
    0 0 28px rgba(200, 40, 140, 0.85),
    0 0 46px rgba(170, 20, 120, 0.75),
    0 0 70px rgba(140, 10, 95, 0.65);
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
    st.markdown(
        "## View sales charts\n"
        "View detailed information in charts of video game sales over time and filter by region."
    )
    sales_on = st.toggle(TOGGLE_SALES_LABEL)

with col2:
    st.caption("") # Empty line to align with design
    spacer, right = st.columns([1, 1])
    with right:
        region = st.radio(REGION_RADIO_LABEL, REGIONS)

try:
    sales_col = get_sales_column(region, REGION_COLUMN_MAP)
except ValueError as e:
    st.error(str(e))
    st.stop()

st.session_state.region = region


# =======================
# YEAR SLIDER (NO AGE FILTER)
# =======================
years = validate_years(df["Year"].dropna().unique())
year_min, year_max = min(years), max(years)

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

    try:
        min_sales = validate_min_sales(min_sales)
    except ValueError as e:
        st.warning(str(e))
        st.stop()

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
