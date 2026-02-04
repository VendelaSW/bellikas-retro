import streamlit as st
from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import filter_sales
from bellikas_retro.utils.config import REGION_COLUMN_MAP, REGIONS, TOGGLE_SALES_LABEL, YEAR_SLIDER_LABEL

init_session_state()
df = load_data()

st.title("Top Sellers")

# Controls
col1, col2 = st.columns(2)
with col1:
    sales_on = st.toggle(TOGGLE_SALES_LABEL)
with col2:
    region = st.radio("Select region", REGIONS)

sales_col = REGION_COLUMN_MAP[region]
st.session_state.region = region

years = sorted(df["Year"].dropna().unique())
selected_year = st.select_slider(
    YEAR_SLIDER_LABEL, 
    options=years, 
    value=years[0])

# =======================
# FILTER DATA
# =======================

filtered_df = df[df["Year"] == selected_year].copy()

if sales_on:
    max_sales = float(filtered_df[sales_col].max() or 0.0)

    min_sales = st.slider(
        "Minimum sales (millions)",
        min_value=0.0,
        max_value=max(1.0, round(max_sales, 1)),
        value=1.0,
        step=0.1,
        format="%.1f",
        key="top_min_sales"
    )

    filtered_df = filter_sales(
        df=filtered_df,
        region=sales_col,
        minimum=min_sales,
    )

st.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]]
    .sort_values(by=sales_col, ascending=False),
    hide_index=True,
)