import streamlit as st
import plotly.express as px
from utils import load_data, create_age_group

st.title("Age Group Susceptibility")

df = load_data()
df = create_age_group(df)

# UI Component 1: Slider
age_limit = st.slider("Maximum Age", 10,100,100)

df = df[df["AGE"] <= age_limit]

age_cases = df["AGE_GROUP"].value_counts().sort_index()

fig = px.bar(
    x=age_cases.index.astype(str),
    y=age_cases.values,
    labels={"x":"Age Group","y":"Cases"},
    title="COVID Cases by Age Group"
)

st.plotly_chart(fig)


# UI Component 3: Button
if st.button("Generate Report"):

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Report",
        data=csv,
        file_name="Age_Analysis_report.csv",
        mime="text/csv"
    )
