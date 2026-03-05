import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
import io

st.title("Q1: Age Groups Most Susceptible to COVID-19")

df = load_data()

# Age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins)

# Count per age group
age_counts = df["AGE_GROUP"].value_counts().sort_index()
age_counts_df = age_counts.reset_index()
age_counts_df.columns = ["Age Group","Number of Cases"]

# Bar chart
fig = px.bar(
    x=age_counts_df["Age Group"].astype(str),
    y=age_counts_df["Number of Cases"],
    labels={"x":"Age Group","y":"Number of Cases"},
    text=age_counts_df["Number of Cases"],
    title="Number of Cases by Age Group"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)

# Show table
st.dataframe(age_counts_df)

# ✅ Download button
csv_buffer = io.StringIO()
age_counts_df.to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q1_age_report.csv",
    mime="text/csv"
)
