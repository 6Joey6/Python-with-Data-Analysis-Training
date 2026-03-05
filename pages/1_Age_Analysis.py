import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
import io

st.title("Q1: Age Groups Most Susceptible to COVID-19")

# Load data
df = load_data()

# Define age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]

# Define human-readable labels
labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]  # 0-9, 10-19, etc.

# Create AGE_GROUP column
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=False)

# Count per age group
age_counts = df["AGE_GROUP"].value_counts().sort_index()
age_counts_df = age_counts.reset_index()
age_counts_df.columns = ["Age Group","Number of Cases"]

# Bar chart
fig = px.bar(
    x=age_counts_df["Age Group"],
    y=age_counts_df["Number of Cases"],
    labels={"x":"Age Group","y":"Number of Cases"},
    text=age_counts_df["Number of Cases"],
    title="Number of Cases by Age Group"
)
fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=-45)  # rotate labels for readability
st.plotly_chart(fig)

# Show table
st.dataframe(age_counts_df)

# ✅ CSV Download button
csv_buffer = io.StringIO()
age_counts_df.to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q1_age_report.csv",
    mime="text/csv"
)
