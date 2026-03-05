# Only rows with YES/NO
import streamlit as st
import pandas as pd
import plotly.express as px
import io
from utils import load_data

st.set_page_config(page_title="Q3: Intubation Analysis")

st.title("Q3: Patients Requiring Intubation")

# Load dataset
df = load_data()

# Check dataset values (optional debug)
# st.write(df["INTUBATED"].unique())

# Only include rows where INTUBATED is YES or NO
intubated_df = df[df["INTUBATED"].isin(["YES","NO"])]

# Count YES/NO
intubated_counts = intubated_df["INTUBATED"].value_counts().reset_index()
intubated_counts.columns = ["Intubation Status", "Number of Patients"]

# --- Plotly Pie Chart ---
fig = px.pie(
    intubated_counts,
    names="Intubation Status",
    values="Number of Patients",
    title="Proportion of Patients Requiring Intubation",
    hole=0.4,  # Donut chart
    color="Intubation Status",
    color_discrete_map={"YES":"red", "NO":"green"}
)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig)

# --- Show Table ---
st.subheader("Intubation Counts")
st.dataframe(intubated_counts)

# --- Download Button ---
csv_buffer = io.StringIO()
intubated_counts.to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Report as CSV",
    data=csv_buffer.getvalue(),
    file_name="q3_intubation_report.csv",
    mime="text/csv"
)
