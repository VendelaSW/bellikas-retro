import streamlit as st

pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/nostalgia.py", title="Nostalgia"),
        st.Page("pages/top.py", title="Top"),
        st.Page("pages/charts.py", title="Charts"),
    ],
    position="top"
)

st.markdown(
    """
    <style>
      .block-container {
        padding-top: 1rem;
      }
      .stAppHeader {
      background: transparent !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

pg.run()
