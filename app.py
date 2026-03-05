import streamlit as st

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

from PIL import Image
logo = Image.open("logo.png")
st.sidebar.image(logo, use_column_width=True)

st.title("COVID-19 Dashboard - Fourtitude")

st.markdown("""
Use the sidebar to navigate between pages:
- Question 1: Age group susceptibility
- Question 2: Gender & Age distribution
- Question 3: Patients Required Intubation 
- Question 4: Correlations Between Diseases and ICU Admission
- Question 5: Common Diseases in Deceased Patients
""")


