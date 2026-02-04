from pathlib import Path
import pandas as pd
import streamlit as st

from bellikas_retro.data_loader import download_dataset, DataLoader

REGION_MAP = {
    "NA": "NA_Sales",
    "EU": "EU_Sales",
    "JP": "JP_Sales",
    "OTHER": "Other_Sales",
    "GLOBAL": "Global_Sales",
}

def init_session_state():
    for key in ["region", "year_range"]:
        if key not in st.session_state:
            st.session_state[key] = None

@st.cache_data
def load_data() -> pd.DataFrame:
    download_dataset()
    loader = DataLoader(data_dir=Path("data"))
    df = loader.load()
    return pd.DataFrame(df)
