import streamlit as st
import pandas as pd

st.set_page_config(page_title="COVID Dashboard", layout="wide")

# Logo
st.image("logo.png", width=200)

st.title("COVID-19 Analysis Dashboard")

st.write("""
This dashboard analyzes COVID-19 patient data.

Features:
- Age susceptibility analysis
- Gender vs Age distribution
- Interactive charts
- Downloadable reports
""")

st.sidebar.header("Navigation")

st.success("Use the sidebar to navigate between pages.")
