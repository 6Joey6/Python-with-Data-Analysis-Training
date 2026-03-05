# pages/3_Intubation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Q3: Patients Requiring Intubation")

df = load_data()

# Count yes/no
intubated_counts = df["INTUBATED"].map({1:"YES", 2:"NO"}).value_counts()

# Donut chart
fig = px.pie(
    names=intubated_counts.index,
    values=intubated_counts.values,
    title="Proportion of Patients Requiring Intubation",
    hole=0.4
)
st.plotly_chart(fig)
st.dataframe(intubated_counts)
