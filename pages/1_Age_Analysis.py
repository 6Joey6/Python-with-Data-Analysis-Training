import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 1: Most Susceptible Age Groups")

df = load_data()

# Slider for selecting age range
age_range = st.slider("Select Age Range", 0, 100, (0, 100))
df_filtered = df[(df["AGE"] >= age_range[0]) & (df["AGE"] <= age_range[1])]

# Age binning
bins = [0,10,20,30,40,50,60,70,80,90,100]
labels = ["0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"]
df_filtered["AGE_GROUP"] = pd.cut(df_filtered["AGE"], bins=bins, labels=labels, right=False)

age_counts = df_filtered["AGE_GROUP"].value_counts().sort_index()

# Interactive bar chart
fig = px.bar(
    x=age_counts.index,
    y=age_counts.values,
    labels={"x":"Age Group", "y":"Number of Cases"},
    title="COVID-19 Cases by Age Group"
)
st.plotly_chart(fig)

# Download report button
st.download_button(
    label="Download Age Group Report",
    data=age_counts.to_csv().encode("utf-8"),
    file_name="age_group_report.csv",
    mime="text/csv"
)
