# pages/5_Deceased_Diseases.py
import streamlit as st
from utils import load_data
import pandas as pd
import plotly.express as px

st.title("Question 5: Common Diseases Among Deceased Patients")

df = load_data()

# Filter deceased patients
deceased = df[df["DATE_OF_DEATH"].notna()]

# Disease list
diseases = [
    "DIABETES","COPD","ASTHMA","INMUSUPR",
    "HYPERTENSION","CARDIOVASCULAR",
    "OBESITY","CHRONIC_KIDNEY","TOBACCO"
]

# Count how many deceased had each disease
disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (deceased[disease] == 1).sum()  # 1 = YES

cross_tab = pd.DataFrame.from_dict(disease_counts, orient="index", columns=["Deceased Patients"])
cross_tab.index.name = "Disease"
cross_tab.reset_index(inplace=True)

# Plot bar chart
fig = px.bar(
    cross_tab,
    x="Disease",
    y="Deceased Patients",
    text="Deceased Patients",
    labels={"Disease":"Disease","Deceased Patients":"Number of Deceased Patients"},
    title="Diseases Among Deceased Patients"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)

st.subheader("Data Table")
st.dataframe(cross_tab)
