import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
import io

st.title("Q4: Correlation Between Diseases and ICU Admission")

df = load_data()

diseases = ["DIABETES","COPD","ASTHMA","INMUSUPR",
            "HYPERTENSION","CARDIOVASCULAR","OBESITY",
            "CHRONIC_KIDNEY","TOBACCO"]

icu_patients = df[df["ICU"] == 1]

disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (icu_patients[disease] == 1).sum()

cross_tab = pd.DataFrame.from_dict(disease_counts, orient="index", columns=["ICU Patients"])
cross_tab.index.name = "Disease"
cross_tab.reset_index(inplace=True)

# Clustered bar chart
fig = px.bar(
    cross_tab,
    x="Disease",
    y="ICU Patients",
    text="ICU Patients",
    title="Number of ICU Patients with Each Disease"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)
st.dataframe(cross_tab)


csv_buffer = io.StringIO()
cross_tab.to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q4_icu_disease_report.csv",
    mime="text/csv"
)

