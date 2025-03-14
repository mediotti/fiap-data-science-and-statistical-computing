from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="Greeting Dashboard - Gabriel Mediotti", layout="wide")
st.sidebar.markdown("Desenvolvido por Gabriel Mediotti - [Github](https://github.com/mediotti)")

col1, col2 = st.columns(2)

with col1:
    st.write(Path("../assets/whoami.md").read_text())

with col2:
    st.image("../assets/me.png")