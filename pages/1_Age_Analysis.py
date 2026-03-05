import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Q1: Age Groups Most Susceptible to COVID-19")

df = load_data()

# Age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins)

# Count per age group
age_counts = df["AGE_GROUP"].value_counts().sort_index()

# Bar chart
fig = px.bar(
    x=age_counts.index.astype(str),
    y=age_counts.values,
    labels={"x":"Age Group","y":"Number of Cases"},
    text=age_counts.values,
    title="Number of Cases by Age Group"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)
st.dataframe(age_counts)
