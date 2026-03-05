import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 4: Correlation Between Diseases and ICU Admission")

df = load_data()

# List of diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Filter valid ICU records
df = df[df["ICU"].isin(["YES","NO"])]

# UI: select disease
disease_selected = st.selectbox("Select a Disease", diseases)

# Disease vs ICU cross-tab
df_disease = df[df[disease_selected].isin(["YES","NO"])]
cross_tab = pd.crosstab(df_disease[disease_selected], df_disease["ICU"])

st.subheader(f"ICU Admission vs {disease_selected}")
st.dataframe(cross_tab)

# Interactive stacked bar chart
fig = px.bar(
    cross_tab,
    x=cross_tab.index,
    y=["YES","NO"],
    title=f"{disease_selected} vs ICU Admission",
    labels={"value":"Number of Patients", "x":disease_selected},
    text_auto=True
)
st.plotly_chart(fig)

# Download report
st.download_button(
    label=f"Download {disease_selected} vs ICU Report",
    data=cross_tab.to_csv().encode("utf-8"),
    file_name=f"{disease_selected}_icu_report.csv",
    mime="text/csv"
)
