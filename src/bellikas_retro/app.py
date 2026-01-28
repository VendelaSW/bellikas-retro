"""
Bellika's Retro - Skeleton Streamlit App
"""
from bellikas_retro.data_loader import download_dataset, DataLoader
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bellika's Retro", layout="centered")

html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  :root{
    --neon: #2aa8ff;        /* blå neon */
    --neon2: #7fd6ff;       /* ljusare blå */
    --bg: transparent;
  }

  body{
    margin:0;
    background: var(--bg);
    display:flex;
    align-items:center;
    justify-content:center;
    height: 220px;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }

  .sign-wrap{
    padding: 24px 28px;
    border-radius: 18px;
    background: rgba(0,0,0,0.25);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    backdrop-filter: blur(6px);
  }

  .neon{
    position: relative;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: clamp(28px, 5vw, 56px);
    color: var(--neon2);
    text-shadow:
      0 0 6px rgba(42,168,255,0.8),
      0 0 18px rgba(42,168,255,0.55),
      0 0 42px rgba(42,168,255,0.35);
    /* subtil “rörlighet” i ljuset */
    animation: flicker 3.8s infinite;
  }

  /* “Rörligt neonljus som rör sig runt i bokstäverna”:
     Vi lägger en animerad gradient ovanpå texten och clippar till bokstäverna */
  .neon::after{
    content: "BELLIKA'S RETRO";
    position:absolute;
    inset: 0;
    color: transparent;
    background: linear-gradient(
      110deg,
      rgba(0,0,0,0) 0%,
      rgba(127,214,255,0.05) 20%,
      rgba(127,214,255,0.9) 35%,
      rgba(42,168,255,0.7) 45%,
      rgba(127,214,255,0.9) 55%,
      rgba(127,214,255,0.05) 70%,
      rgba(0,0,0,0) 100%
    );
    background-size: 220% 100%;
    -webkit-background-clip: text;
    background-clip: text;

    filter: drop-shadow(0 0 10px rgba(42,168,255,0.8))
            drop-shadow(0 0 26px rgba(42,168,255,0.45));

    animation: sweep 1.9s linear infinite;
    mix-blend-mode: screen;
    pointer-events:none;
  }

  /* Extra “kantglöd” runt bokstäverna som pulserar */
  .neon::before{
    content: "BELLIKA'S RETRO";
    position:absolute;
    inset: 0;
    color: transparent;
    -webkit-text-stroke: 2px rgba(42,168,255,0.35);
    text-stroke: 2px rgba(42,168,255,0.35);
    filter: drop-shadow(0 0 12px rgba(42,168,255,0.65));
    animation: pulse 2.6s ease-in-out infinite;
    pointer-events:none;
  }

  @keyframes sweep{
    0%   { background-position: 0% 50%;   opacity: 0.75; }
    50%  { background-position: 100% 50%; opacity: 1.00; }
    100% { background-position: 0% 50%;   opacity: 0.75; }
  }

  @keyframes pulse{
    0%,100% { opacity: 0.55; }
    50%     { opacity: 0.95; }
  }

  /* Lätt neon-flicker (inte för aggressiv) */
  @keyframes flicker{
    0%, 100% { opacity: 1; }
    2%  { opacity: 0.95; }
    3%  { opacity: 1; }
    7%  { opacity: 0.92; }
    8%  { opacity: 1; }
    72% { opacity: 0.98; }
    73% { opacity: 0.90; }
    74% { opacity: 1; }
  }
</style>
</head>

<body>
  <div class="sign-wrap" aria-label="Neon banner">
    <div class="neon">BELLIKA'S RETRO</div>
  </div>
</body>
</html>
"""

components.html(html, height=240)

download_dataset()
# ====================
# SESSION STATE
# ====================
for key in ["region", "year_range"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ====================
# DATA LOADING
# ====================
@st.cache_data
def load_data():
    # Placeholder for real CSV load
    # df = pd.read_csv("video_game_sales.csv")
    loader = DataLoader(data_dir=Path("data"))

    df = loader.load()
    return pd.DataFrame(df)

df = load_data()

# ====================
# LAYOUT
# ====================
st.title("Bellika's Retro: Retro Game Sales Dashboard")

# Sidebar controls
st.sidebar.header("Filters")

# Slider for year range
year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
st.session_state.year_range = st.sidebar.slider(
    "Select release year range",
    year_min, year_max, (year_min, year_max)
)

# Select region
st.session_state.region = st.sidebar.radio(
    "Select region to display sales",
    ("NA", "EU", "JP")
)

# ====================
# FILTER DATA
# ====================
filtered_df = df[
    (df["Year"] >= st.session_state.year_range[0]) &
    (df["Year"] <= st.session_state.year_range[1])
]

# Map region selection to sales column
region_map = {
    "NA": "NA_Sales",
    "EU": "EU_Sales",
    "JP": "JP_Sales"
}
sales_col = region_map[st.session_state.region]

# ====================
# MAIN DISPLAY
# ====================
st.header(f"Top Games by {st.session_state.region} Sales")

st.dataframe(
    filtered_df[["Rank", "Name", "Platform", "Year", sales_col]].sort_values(
        by=sales_col, ascending=False
    )
)

# Placeholder for map (could later use plotly or pydeck)
st.header(f"Interactive Sales Map ({st.session_state.region})")
st.write("Map feature coming here... for now just a placeholder")

# ====================
# FUTURE FEATURES
# ====================
st.write("Additional features can be added here: charts, graphs, or interactive maps.")
