import streamlit as st
from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
from bellikas_retro.utils.config import TOGGLE_SALES_LABEL, REGION_COLUMN_MAP, REGIONS, AGE_INPUT_LABEL, MAX_AGE, MIN_AGE
init_session_state()
df = load_data()

st.title("Nostalgia", anchor="nostalgia")

st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

#nostalgia {
  margin-top: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 4rem;
  color: #fff6f6;

  -webkit-text-stroke: 0.7px rgba(255, 230, 230, 0.55);
  -webkit-font-smoothing: antialiased;

  animation: flicker 3.0s infinite;

  text-shadow:
    0 0 1px rgba(255,255,255,0.9),
    0 0 3px rgba(255,210,210,0.7),
    0 0 8px rgba(255, 40, 40, 0.95),
    0 0 16px rgba(255, 0, 0, 0.85),
    0 0 28px rgba(220, 0, 0, 0.65),
    0 0 46px rgba(160, 0, 0, 0.55),
    0 0 70px rgba(120, 0, 0, 0.45);
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

# Controls
col1, col2 = st.columns(2)
with col1:
    sales_on = st.toggle(TOGGLE_SALES_LABEL)
with col2:
    region = st.radio("Select region", REGIONS)

sales_col = REGION_COLUMN_MAP[region]
st.session_state.region = region

age_input = st.number_input(
    AGE_INPUT_LABEL,
    min_value=MIN_AGE, 
    max_value=MAX_AGE, 
    value=25
)
age_range = nostalgia_age_filter(int(age_input))

filtered_df = df[df["Year"].isin(age_range)].copy()

# =======================
# FILTER DATA
# =======================

if sales_on:
    max_sales = float(filtered_df[sales_col].max() or 0.0)

    min_sales = st.slider(
        "Minimum sales (millions)",
        min_value=0.0,
        max_value=max(1.0, round(max_sales, 1)),
        value=1.0,
        step=0.1,
        format="%.1f",
        key="nostalgia_min_sales"
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
