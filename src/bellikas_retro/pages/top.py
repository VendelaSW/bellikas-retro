import streamlit as st
from bellikas_retro.app_state import init_session_state, load_data, REGION_MAP
from bellikas_retro.utils.helpers import filter_sales

init_session_state()
df = load_data()

st.title("Top Sellers", anchor="top")

st.markdown(
"""
<style>
#top {
  color: #e2b3ff;
  font-weight: 700;
  animation: flicker 2.3s infinite alternate;
  text-shadow:
    0 0 4px #ffffff,
    0 0 12px rgba(214,107,255,0.9),
    0 0 36px rgba(154,28,255,0.6);
}

@keyframes flicker {
  0% { opacity: 1; }
  45% { opacity: .9; }
  50% { opacity: .7; }
  55% { opacity: .95; }
  100% { opacity: 1; }
}
</style>

""",
unsafe_allow_html=True,
)

# Controls
col1, col2 = st.columns(2)
with col1:
    sales_on = st.toggle("Activate Min Sales Filter")
with col2:
    region = st.radio("Select region", ("NA", "EU", "JP", "OTHER", "GLOBAL"))

sales_col = REGION_MAP[region]
st.session_state.region = region

years = sorted(df["Year"].dropna().unique())
selected_year = st.select_slider("Release Year", options=years, value=years[0])

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