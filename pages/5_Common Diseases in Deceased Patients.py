import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
import io

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

csv_buffer = io.StringIO()
data_to_download = cross_tab  # replace with the DF you want to allow download
data_to_download.to_csv(csv_buffer, index=False)

# Add download button
st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q5_deceased_disease_report.csv",  # replace qX with question number
    mime="text/csv"
)

