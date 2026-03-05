import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from fpdf import FPDF
import io

st.set_page_config(page_title="Q5: Deceased Patients Diseases")

st.title("Q5: Common Diseases Among Deceased Patients")

df = load_data()

# Keep only patients with a date of death
df_deceased = df[df["DATE_OF_DEATH"].notna()]

# List of diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Count how many deceased had each disease
disease_counts = {}
for disease in diseases:
    disease_counts[disease] = (df_deceased[disease] == "YES").sum()

disease_df = pd.DataFrame(list(disease_counts.items()), columns=["Disease","Number of Deceased Patients"])

# Plot bar chart
fig = px.bar(
    disease_df,
    x="Disease",
    y="Number of Deceased Patients",
    title="Common Diseases Among Deceased Patients",
    text_auto=True
)
st.plotly_chart(fig)

st.dataframe(disease_df)

# --- Download PDF report ---
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Deceased Patients Disease Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Disease", 1)
    pdf.cell(80, 10, "Number of Deceased Patients", 1)
    pdf.ln()
    pdf.set_font("Arial", "", 12)
    for i, row in df.iterrows():
        pdf.cell(80, 10, str(row["Disease"]), 1)
        pdf.cell(80, 10, str(row["Number of Deceased Patients"]), 1)
        pdf.ln()
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

pdf_bytes = create_pdf(disease_df)
st.download_button(
    label="Download Deceased Disease PDF",
    data=pdf_bytes,
    file_name="deceased_disease_report.pdf",
    mime="application/pdf"
)
