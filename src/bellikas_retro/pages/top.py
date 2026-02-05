import streamlit as st
from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import filter_sales
from bellikas_retro.utils.config import REGION_COLUMN_MAP, REGIONS, TOGGLE_SALES_LABEL, YEAR_SLIDER_LABEL

init_session_state()
df = load_data()
if df.empty:
    st.warning("Dataset not available in this environment.")
    st.stop()

st.title("Top Sellers", anchor="top")

st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

#top {
  margin-top: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 4rem;
  color: #e3ebff;

  -webkit-text-stroke: 0.7px rgba(200, 215, 255, 0.6);
  -webkit-font-smoothing: antialiased;

  animation: flicker 3.0s infinite;

  text-shadow:
    0 0 1px rgba(255,255,255,0.55),
    0 0 3px rgba(200,220,255,0.45),
    0 0 8px rgba(60, 140, 255, 1),
    0 0 16px rgba(30, 110, 255, 0.95),
    0 0 28px rgba(20, 80, 220, 0.75),
    0 0 46px rgba(10, 60, 180, 0.65),
    0 0 70px rgba(5, 40, 140, 0.55);
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