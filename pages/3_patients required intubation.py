import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 3: Patients Requiring Intubation")

df = load_data()

# Filter valid intubation records
df_intubated = df[df["INTUBATED"].isin(["YES", "NO"])]

# Count
intubation_counts = df_intubated["INTUBATED"].value_counts()

# Pie chart
fig = px.pie(
    names=intubation_counts.index,
    values=intubation_counts.values,
    title="Intubation Requirement"
)
st.plotly_chart(fig)

st.dataframe(intubation_counts)

# Download report
st.download_button(
    label="Download Intubation Report",
    data=intubation_counts.to_csv().encode("utf-8"),
    file_name="intubation_report.csv",
    mime="text/csv"
)
