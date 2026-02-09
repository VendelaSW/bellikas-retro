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
@import url('https://fonts.googleapis.com/css2?family=Neonderthaw&display=swap');

/* Center the whole block */
div[data-testid="stMarkdownContainer"] .title-wrapper {
  display: flex;
  justify-content: center;
}

/* ===== INFO BOX (retro panel) ===== */
div[data-testid="stMarkdownContainer"] .box {
  margin: 60px auto 0;
  padding: 14px 20px;
  padding-top: 8px;
  max-width: 420px;

  background: rgba(0, 0, 0, 0.85);

  border-radius: 14px;
  border: 2px solid rgba(120, 170, 255, 0.35);

  box-shadow:
    0 0 6px rgba(80, 140, 255, 0.35),
    0 0 18px rgba(40, 110, 255, 0.25),
    inset 0 0 12px rgba(255,255,255,0.05);

  color: #e8ecff;
  text-align: center;
}

div[data-testid="stMarkdownContainer"] .box ul {
  list-style: none;
  padding: 0;
  margin: 0;
  margin-bottom: 12px;
}

/* Dashboard title = biggest */
div[data-testid="stMarkdownContainer"] .box h3,
div[data-testid="stMarkdownContainer"] .box h3 span {
  display: block;
  text-align: center;
  margin: 0 0 8px 0;
  margin-bottom: 0;
  font-size: 2.3rem !important;
  font-variant: small-caps;
  letter-spacing: 0.12em;
  font-weight: 650;
  color: rgba(235, 245, 255, 0.95) !important;
  text-shadow: 0 0 3px rgba(120, 160, 220, 0.2);
}

/* “Use the top menu…” */
div[data-testid="stMarkdownContainer"] .box > span {
  display: block !important;
  margin-top: -30px !important;
  margin-bottom: 10px;

  font-size: 1.2rem !important;
  font-variant: small-caps;
  letter-spacing: 0.1em;
  font-weight: 550;

  color: rgba(120, 150, 210, 0.95) !important;
  text-shadow: 0 0 3px rgba(80, 120, 190, 0.22);
}

/* List items = smallest */
div[data-testid="stMarkdownContainer"] .box li {
  margin: 2px 0;
  line-height: 1.5;

  font-size: 0.95rem !important;
  font-variant: small-caps;
  letter-spacing: 0.08em;
  font-weight: 520;

  color: rgba(210, 225, 255, 0.95) !important;
  text-shadow: 0 0 3px rgba(150, 190, 255, 0.2);
}

/* ===== NEON TITLE PANEL (blue frame) ===== */
div[data-testid="stMarkdownContainer"] .title-panel {
  display: inline-block;
  width: fit-content;
  box-sizing: border-box;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: borderGlowFlicker 4.8s infinite;
  overflow: hidden;

  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 0.2px;
  padding-right: 0.2px;

  background: rgba(0,0,0,0);
  border-style: solid;
  border-color: #eaf0ff;
  border-width: 8px;
  border-radius: 16px;

  box-shadow:
    0 0 1px rgba(255,255,255,0.5),
    0 0 4px rgba(180,210,255,0.6),
    0 0 10px rgba(80,140,255,0.9),
    0 0 20px rgba(40,110,255,0.85),
    0 0 35px rgba(20,80,220,0.7),
    0 0 55px rgba(10,60,180,0.6),

    0 0 1px inset rgba(255,255,255,0.4),
    0 0 4px inset rgba(180,210,255,0.5),
    0 0 10px inset rgba(80,140,255,0.85),
    0 0 20px inset rgba(40,110,255,0.75),
    0 0 35px inset rgba(20,80,220,0.65),
    0 0 55px inset rgba(10,60,180,0.55);
}

/* The neon title */
div[data-testid="stMarkdownContainer"] .title-panel h1 {
  white-space: nowrap;
  display: inline-block;
  margin-left: -45px;
  margin-right: 1px;
  font-family: 'Neonderthaw', cursive !important;
  font-size: 7rem !important;
  color: #ffb0b0 !important;
  transform: translate(4px, -6px) scaleX(0.8);
  line-height: 0.9;
  width: max-content;

  -webkit-text-stroke: 0.5px rgba(255,235,220,0.55);
  -webkit-font-smoothing: antialiased;

  animation: flicker 3.0s infinite;

text-shadow:
  0 0 2px rgba(255, 0, 0, 1),
  0 0 4px rgba(255, 10, 20, 1),
  0 0 10px rgba(235, 0, 10, 0.95),
  0 0 28px rgba(120, 20, 55, 0.8),
  0 0 46px rgba(95, 12, 40, 0.7),
  0 0 70px rgba(70, 8, 30, 0.6);
}

@keyframes flicker {
  0%, 38%, 100% { opacity: 1; }
  40% { opacity: 0.9; }
  41% { opacity: 0.75; }
  42% { opacity: 1; }
  78% { opacity: 0.95; }
}

@keyframes borderGlowFlicker {
  0%, 80%, 100% { filter: brightness(1); }
  82% { filter: brightness(0.85); }
  84% { filter: brightness(1.05); }
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
    <span>Use the top menu to explore:</span>
 <ul>
  <li>&#x2022; Nostalgia: Filter releases based on your age</li>
    <li>&#x2022; Top: Top sellers by region + filters</li>
      <li>&#x2022; Charts: Sales trends over time</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
