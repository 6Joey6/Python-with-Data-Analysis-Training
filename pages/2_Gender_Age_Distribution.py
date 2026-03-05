# pages/2_Gender_Age_Distribution.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Q2: Distribution of Cases by Gender & Age Group")

df = load_data()

# Map SEX codes
df["SEX"] = df["SEX"].map({1:"FEMALE", 2:"MALE", 99:"UNKNOWN"})

# Age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins)

# Drop rows with null SEX or AGE_GROUP
df = df.dropna(subset=["SEX", "AGE_GROUP"])

# Sunburst chart: Gender -> Age Group
fig = px.sunburst(
    df,
    path=["SEX", "AGE_GROUP"],
    title="Cases Distribution by Gender & Age Group"
)

st.plotly_chart(fig)
