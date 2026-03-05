import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
from utils import load_data
import io
import tempfile

st.title("Q3: Patients Requiring Intubation")

# Load data
df = load_data()

# Keep rows with INTUBATED values
intubated_df = df[df["INTUBATED"].notna()]

# Count each category
intubated_counts = intubated_df["INTUBATED"].value_counts().reset_index()
intubated_counts.columns = ["Intubation Status", "Number of Patients"]

# --- Interactive Plotly Pie Chart ---
fig = px.pie(
    intubated_counts,
    names="Intubation Status",
    values="Number of Patients",
    title="Patients Requiring Intubation (Current Dataset)",
    hole=0.4
)
st.plotly_chart(fig)

# --- Show Table ---
st.dataframe(intubated_counts)

# ------------------- PDF Generation -------------------
def create_pdf_with_chart(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Patients Requiring Intubation", ln=True, align="C")
    pdf.ln(5)

    # --- Matplotlib Pie Chart for PDF ---
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(
        df["Number of Patients"],
        labels=df["Intubation Status"],
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Set3.colors
    )
    ax.set_title("Patients Requiring Intubation")
    plt.tight_layout()

    # Save chart to temporary PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name, format="png", dpi=150)
        tmpfile_path = tmpfile.name

    # Insert chart into PDF
    chart_y = 30
    pdf.image(tmpfile_path, x=40, y=chart_y, w=130)

    # --- Table below chart ---
    chart_height_mm = 100
    pdf.set_y(chart_y + chart_height_mm + 10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Intubation Status", 1)
    pdf.cell(80, 10, "Number of Patients", 1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 12)
    for i, row in df.iterrows():
        pdf.cell(80, 10, str(row["Intubation Status"]), 1)
        pdf.cell(80, 10, str(int(row["Number of Patients"])), 1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# Generate PDF and provide download button
pdf_bytes = create_pdf_with_chart(intubated_counts)
st.download_button(
    label="Download PDF (With Chart)",
    data=pdf_bytes,
    file_name="q3_intubation_report.pdf",
    mime="application/pdf"
)
