from .utils import DATA_DIR, CSV_NAME
import pandas as pd
import streamlit as st

from bellikas_retro.data_loader import download_dataset, DataLoader
from bellikas_retro.utils.config import SESSION_KEYS

def init_session_state():
    for key in SESSION_KEYS:
        if key not in st.session_state:
            st.session_state[key] = None

@st.cache_data
def load_data() -> pd.DataFrame:
    download_dataset()

    data_dir = DATA_DIR
    csv_path = DATA_DIR / CSV_NAME

    # If download was skipped (CI) and file isn't present, prevent crash.
    if not csv_path.exists():
        return pd.DataFrame()

    loader = DataLoader(data_dir=data_dir)
    df = loader.load()
    return pd.DataFrame(df)