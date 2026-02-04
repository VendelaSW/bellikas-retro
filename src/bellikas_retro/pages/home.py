import streamlit as st
from bellikas_retro.app_state import init_session_state
from bellikas_retro.utils import PROJECT_ROOT
from bellikas_retro.utils.config import NEON_IMAGE_PATH

init_session_state()

st.image(
    image=PROJECT_ROOT / NEON_IMAGE_PATH,
    width="stretch",
)

st.title("Bellika's Retro: Retro Game Sales Dashboard")

st.write(
    """
    Welcome! Use the sidebar to explore:
    - **Nostalgia**: filter releases based on your age
    - **Top**: top sellers by region + filters
    """
)
