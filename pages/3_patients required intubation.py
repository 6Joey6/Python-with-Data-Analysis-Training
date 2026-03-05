# pages/3_Intubation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
import io

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

csv_buffer = io.StringIO()
data_to_download = cross_tab  # replace with the DF you want to allow download
data_to_download.to_csv(csv_buffer, index=False)

# Add download button
st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q3_intubation_report.csv",  # replace qX with question number
    mime="text/csv"
)

