import base64
import streamlit as st
from bellikas_retro.app_state import init_session_state
from bellikas_retro.utils import PROJECT_ROOT
from bellikas_retro.utils.config import NEON_IMAGE_PATH

init_session_state()

image_path = PROJECT_ROOT / NEON_IMAGE_PATH
with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

/* Center the whole block */
div[data-testid="stMarkdownContainer"] .title-wrapper {
  display: flex;
  justify-content: center;
}

div[data-testid="stMarkdownContainer"] .box {
    margin-top: 40px;
    display: flex;
    flex-direction: column;
  justify-content: center;
    align-items: center;
    background: rgba(0,0,0,0.50);
    border-radius: 20px;
    border-style: solid;
    border-width: 5px;
    border-color: black;

}

/* The black panel */
div[data-testid="stMarkdownContainer"] .title-panel {
  display: inline-flex;
  flex-direction: column;
  align-items: center;

  padding: 40px;
  padding-top: 25px;
  padding-bottom: 5px;
  background: rgba(0,0,0,0);
  border-style: solid;
  border-color: #fff6f6;
  border-width: 10px;
  border-radius: 20px;

  width: fit-content;

  box-shadow:
    0 0 1px rgba(255,255,255,0.9),
    0 0 3px rgba(255,210,210,0.7),
    0 0 8px rgba(255, 40, 40, 0.95),
    0 0 16px rgba(255, 0, 0, 0.85),
    0 0 28px rgba(220, 0, 0, 0.65),
    0 0 46px rgba(160, 0, 0, 0.55),
    0 0 70px rgba(120, 0, 0, 0.45),
    0 0 1px inset rgba(255,255,255,0.9),
    0 0 3px inset rgba(255,210,210,0.7),
    0 0 8px inset rgba(255, 40, 40, 0.95),
    0 0 16px inset rgba(255, 0, 0, 0.85),
    0 0 28px inset rgba(220, 0, 0, 0.65),
    0 0 46px inset rgba(160, 0, 0, 0.55),
    0 0 70px inset rgba(120, 0, 0, 0.45);
}


/* The neon title */
div[data-testid="stMarkdownContainer"] .title-panel h1 {
    white-space: nowrap;
    display: inline-block;
  margin: 0 !important;
  font-family: 'Great Vibes', cursive !important;
  font-size: 8rem !important;
  color: #fff6f6 !important;

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

div[data-testid="stMarkdownContainer"] .title-panel h3 {
  margin: 0 !important;
  margin-top: -10px !important;
  color: rgba(255,255,255,0.85) !important;
  font-size: 2rem !important;
  letter-spacing: 1px;
  text-shadow: 0 0 8px rgba(255,0,0,0.35);
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


st.markdown(
    """
<div class="title-wrapper">
  <div class="title-panel">
    <h1>Bellika's Retro</h1>
   
  </div>
</div>
<div class="box">
    <h3>Retro Game Sales Dashboard</h3>
    <span>Use the sidebar to explore:</span>
 <ul>
  <li>Nostalgia: filter releases based on your age</li>
    <li>Top: top sellers by region + filters</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
