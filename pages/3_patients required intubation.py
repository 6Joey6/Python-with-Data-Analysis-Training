import streamlit as st
import pandas as pd
import plotly.express as px
import io
from utils import load_data

st.title("Q3: Patients Requiring Intubation")

df = load_data()

# Include all mapped INTUBATED values
intubated_df = df[df["INTUBATED"].notna()]

# Count each category
intubated_counts = intubated_df["INTUBATED"].value_counts().reset_index()
intubated_counts.columns = ["Intubation Status", "Number of Patients"]

# Pie chart
fig = px.pie(
    intubated_counts,
    names="Intubation Status",
    values="Number of Patients",
    title="Patients Requiring Intubation (Current Dataset)",
    hole=0.4
)
st.plotly_chart(fig)

# Table
st.dataframe(intubated_counts)

# Download
csv_buffer = io.StringIO()
intubated_counts.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q3_intubation_report.csv",
    mime="text/csv"
)
