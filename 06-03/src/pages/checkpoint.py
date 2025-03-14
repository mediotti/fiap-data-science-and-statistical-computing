import streamlit as st
from pathlib import Path

st.write(Path("../README.md").read_text())