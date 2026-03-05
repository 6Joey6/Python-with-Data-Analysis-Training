import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 2: Distribution by Gender & Age Group")

df = load_data()

# Selectbox for gender filter
gender_filter = st.selectbox("Select Gender", options=["ALL","FEMALE","MALE","UNKNOWN"])

if gender_filter != "ALL":
    df = df[df["SEX"] == gender_filter]

# Age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]
labels = ["0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"]
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=False)

# Interactive stacked bar chart
age_gender = df.groupby(["AGE_GROUP", "SEX"]).size().reset_index(name="Count")

fig = px.bar(
    age_gender,
    x="AGE_GROUP",
    y="Count",
    color="SEX",
    barmode="stack",
    title="COVID Cases by Age Group and Gender"
)
st.plotly_chart(fig)

# Download report
st.download_button(
    label="Download Gender & Age Report",
    data=age_gender.to_csv(index=False).encode("utf-8"),
    file_name="gender_age_report.csv",
    mime="text/csv"
)
