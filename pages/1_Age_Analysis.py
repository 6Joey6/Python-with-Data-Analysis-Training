import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
from utils import load_data
import io
import tempfile

st.title("Q1: Age Groups Most Susceptible to COVID-19")

# Load data
df = load_data()

# Define age bins
bins = [0,10,20,30,40,50,60,70,80,90,100]
labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]  # 0-9, 10-19, etc.
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=False)

# Count per age group
age_counts = df["AGE_GROUP"].value_counts().sort_index()
age_counts_df = age_counts.reset_index()
age_counts_df.columns = ["Age Group","Number of Cases"]

# ------------------- Streamlit display -------------------
# Plotly bar chart
fig = px.bar(
    x=age_counts_df["Age Group"],
    y=age_counts_df["Number of Cases"],
    labels={"x":"Age Group","y":"Number of Cases"},
    text=age_counts_df["Number of Cases"],
    title="Number of Cases by Age Group"
)
fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)

# Show table
st.dataframe(age_counts_df)



# ------------------- PDF Generation with Chart -------------------
def create_pdf_with_chart(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "COVID-19 Cases by Age Group", ln=True, align="C")
    pdf.ln(5)

    # Matplotlib chart for PDF
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Age Group"], df["Number of Cases"], color="skyblue")
    ax.set_title("Number of Cases by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Cases")
    for i, v in enumerate(df["Number of Cases"]):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save figure to temporary PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name, format="png", dpi=150)
        tmpfile_path = tmpfile.name

    # Insert chart into PDF
    chart_y = 25
    pdf.image(tmpfile_path, x=15, y=chart_y, w=180)

    # Table below chart
    chart_height_mm = 100
    pdf.set_y(chart_y + chart_height_mm + 10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Age Group", 1)
    pdf.cell(80, 10, "Number of Cases", 1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 12)
    for i, row in df.iterrows():
        pdf.cell(80, 10, str(row["Age Group"]), 1)
        pdf.cell(80, 10, str(row["Number of Cases"]), 1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# Generate PDF and add download button
pdf_bytes = create_pdf_with_chart(age_counts_df)
st.download_button(
    label="Download PDF (With Chart)",
    data=pdf_bytes,
    file_name="q1_age_report_with_chart.pdf",
    mime="application/pdf"
)
