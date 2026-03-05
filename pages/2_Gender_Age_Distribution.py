import streamlit as st
import pandas as pd
import plotly.express as px
import io
from utils import load_data

st.set_page_config(page_title="Q2: Gender & Age Distribution")

st.title("Q2: Distribution of Cases by Gender & Age Group")

# --- Load dataset ---
df = load_data()

# --- Keep only rows with AGE ---
df_filtered = df.dropna(subset=["AGE"])

# --- Create AGE_GROUP and convert to string labels ---
df_filtered["AGE_GROUP"] = pd.cut(
    df_filtered["AGE"],
    bins=[0,10,20,30,40,50,60,70,80,90,100]
)
df_filtered["AGE_GROUP"] = df_filtered["AGE_GROUP"].astype(str)

# --- Group by SEX and AGE_GROUP ---
age_gender_counts = (
    df_filtered.groupby(["SEX","AGE_GROUP"])
    .size()
    .reset_index(name="Number of Patients")
)

# --- Plot Sunburst Chart ---
fig = px.sunburst(
    age_gender_counts,
    path=["SEX","AGE_GROUP"],
    values="Number of Patients",
    title="Cases Distribution by Gender & Age Group"
)
st.plotly_chart(fig)

# --- Show Table ---
st.subheader("Cases by Gender and Age Group")
st.dataframe(age_gender_counts)

# --- Download CSV ---
csv_buffer = io.StringIO()
age_gender_counts.to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q2_gender_age_report.csv",
    mime="text/csv"
)
