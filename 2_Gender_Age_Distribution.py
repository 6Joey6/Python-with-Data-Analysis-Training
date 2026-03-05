import streamlit as st
import plotly.express as px
from utils import load_data, create_age_group

st.title("Gender & Age Distribution")

df = load_data()
df = create_age_group(df)

# UI Component 2: Selectbox
gender = st.selectbox(
    "Select Gender",
    df["SEX"].unique()
)

filtered = df[df["SEX"] == gender]

# Tabs
tab1, tab2 = st.tabs(["Bar Chart", "Pie Chart"])

with tab1:

    fig = px.histogram(
        filtered,
        x="AGE_GROUP",
        color="SEX",
        title="Age Distribution by Gender"
    )

    st.plotly_chart(fig)


with tab2:

    pie_data = filtered["AGE_GROUP"].value_counts()

    fig2 = px.pie(
        values=pie_data.values,
        names=pie_data.index.astype(str),
        title="Age Group Percentage"
    )

    st.plotly_chart(fig2)



if st.button("Generate Report"):

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Report",
        data=csv,
        file_name="Gender_Age_Distribution.csv",
        mime="text/csv"
    )
