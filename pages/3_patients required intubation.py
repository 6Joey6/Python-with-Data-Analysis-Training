# pages/3_Intubation.py
import streamlit as st
from utils import load_data

st.title("Question 3: Patients Requiring Intubation")

df = load_data()

# Count INTUBATED = 1 (YES)
intubated_count = df[df["INTUBATED"] == 1].shape[0]

st.metric("Patients requiring intubation", intubated_count)
