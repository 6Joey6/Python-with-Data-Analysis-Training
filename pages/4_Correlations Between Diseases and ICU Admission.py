import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 4: Correlation Between Diseases and ICU Admission")

df = load_data()

diseases = [
    "DIABETES","COPD","ASTHMA","INMUSUPR",
    "HYPERTENSION","CARDIOVASCULAR",
    "OBESITY","CHRONIC_KIDNEY","TOBACCO"
]

# Filter ICU patients
icu_patients = df[df["ICU"] == 1]

# Count number of ICU patients with each disease
cross_tab = {}
for disease in diseases:
    cross_tab[disease] = (icu_patients[disease] == 1).sum()

cross_tab = pd.DataFrame.from_dict(cross_tab, orient="index", columns=["ICU Patients"])

# Plot bar chart
fig = px.bar(
    cross_tab,
    x=cross_tab.index,
    y="ICU Patients",
    text_auto=True,
    labels={"x":"Disease", "y":"Number of ICU Patients"},
    title="Correlation Between Diseases and ICU Admission"
)

st.plotly_chart(fig)
st.dataframe(cross_tab)
