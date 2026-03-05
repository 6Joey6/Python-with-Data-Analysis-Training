import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("Q5: Common Diseases Among Deceased Patients")

df = load_data()

# Filter deceased
deceased = df[df["DATE_OF_DEATH"].notna()]

diseases = ["DIABETES","COPD","ASTHMA","INMUSUPR",
            "HYPERTENSION","CARDIOVASCULAR","OBESITY",
            "CHRONIC_KIDNEY","TOBACCO"]

disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (deceased[disease] == 1).sum()

cross_tab = pd.DataFrame.from_dict(disease_counts, orient="index", columns=["Deceased Patients"])
cross_tab.index.name = "Disease"
cross_tab.reset_index(inplace=True)

# Horizontal bar chart
fig = px.bar(
    cross_tab,
    x="Deceased Patients",
    y="Disease",
    orientation="h",
    text="Deceased Patients",
    title="Diseases Among Deceased Patients"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)
st.dataframe(cross_tab)
