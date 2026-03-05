import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Question 5: Common Diseases Among Deceased Patients")

df = load_data()

# Filter deceased patients
df_deceased = df[df["DATE_OF_DEATH"].notna()]

# List of diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Count how many deceased patients had each disease
disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (df_deceased[disease] == "YES").sum()

disease_df = pd.DataFrame(list(disease_counts.items()), columns=["Disease","Number of Deceased Patients"])

# Bar chart
fig = px.bar(
    disease_df,
    x="Disease",
    y="Number of Deceased Patients",
    title="Common Diseases Among Deceased Patients",
    text_auto=True
)
st.plotly_chart(fig)

st.dataframe(disease_df)

# Download report
st.download_button(
    label="Download Deceased Disease Report",
    data=disease_df.to_csv(index=False).encode("utf-8"),
    file_name="deceased_disease_report.csv",
    mime="text/csv"
)
