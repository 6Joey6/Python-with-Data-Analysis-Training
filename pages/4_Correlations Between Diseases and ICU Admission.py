# 4_ICU_Disease_Correlation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 4: Correlation Between Diseases and ICU Admission")

# Load dataset
df = load_data()

# List of diseases to check
diseases = [
    "DIABETES","COPD","ASTHMA","INMUSUPR",
    "HYPERTENSION","CARDIOVASCULAR",
    "OBESITY","CHRONIC_KIDNEY","TOBACCO"
]

# Filter ICU patients (1 = Yes)
icu_patients = df[df["ICU"] == 1]

# Count how many ICU patients had each disease
disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (icu_patients[disease] == 1).sum()  # 1 = YES

# Convert to DataFrame
cross_tab = pd.DataFrame.from_dict(disease_counts, orient="index", columns=["ICU Patients"])
cross_tab.index.name = "Disease"
cross_tab.reset_index(inplace=True)

# Plot interactive bar chart
fig = px.bar(
    cross_tab,
    x="Disease",
    y="ICU Patients",
    text="ICU Patients",
    labels={"Disease":"Disease","ICU Patients":"Number of ICU Patients"},
    title="Number of ICU Patients with Each Disease"
)

fig.update_traces(textposition="outside")  # show numbers above bars
st.plotly_chart(fig)

# Show table below the chart
st.subheader("Data Table")
st.dataframe(cross_tab)
