import streamlit as st
from bellikas_retro.app_state import init_session_state, load_data
from bellikas_retro.utils.helpers import nostalgia_age_filter, filter_sales
from bellikas_retro.utils.config import REGION_RADIO_LABEL, TOGGLE_SALES_LABEL, REGION_COLUMN_MAP, REGIONS, AGE_INPUT_LABEL, MAX_AGE, MIN_AGE
from bellikas_retro.utils.validations import validate_age, get_sales_column, validate_min_sales

init_session_state()

df = load_data()
if df.empty:
    st.warning("Dataset not available in this environment.")
    st.stop()

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

# =======================
# Controls
# =======================

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "## Nostalgia calculator\n"
        "Figure out the perfect games to stock for your target audience."
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

age_input = st.number_input(
    AGE_INPUT_LABEL,
    min_value=MIN_AGE, 
    max_value=MAX_AGE, 
    value=25,
    key="nostalgia_age"
)
try:
    age = validate_age(int(age_input), min_age=MIN_AGE, max_age=MAX_AGE)
except ValueError as e:
    st.warning(str(e))
    st.stop()

age_range = nostalgia_age_filter(int(age))

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

st.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]]
    .sort_values(by=sales_col, ascending=False),
    hide_index=True,
)
