import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data
from fpdf import FPDF
import tempfile

# Page setup
st.set_page_config(page_title="Q4: Disease vs ICU Admission")
st.title("Q4: Correlation Between Diseases and ICU Admission")

# Load dataset
df = load_data()

# List of diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Disease selection
disease_selected = st.selectbox("Select a Disease", diseases)

# Filter rows with valid ICU and disease values
df_filtered = df[df["ICU"].isin(["YES","NO"]) & df[disease_selected].isin(["YES","NO"])]

if df_filtered.empty:
    st.warning(f"No data available for {disease_selected} vs ICU.")
else:
    # Create crosstab
    cross_tab = pd.crosstab(df_filtered[disease_selected], df_filtered["ICU"])
    st.subheader(f"ICU Admission vs {disease_selected}")
    st.dataframe(cross_tab)

    # --- Matplotlib chart ---
    fig, ax = plt.subplots(figsize=(6,4))
    cross_tab.plot(kind='bar', stacked=True, ax=ax, color=['#1f77b4', '#ff7f0e'])
    ax.set_xlabel(disease_selected)
    ax.set_ylabel("Number of Patients")
    ax.set_title(f"{disease_selected} vs ICU Admission")
    plt.xticks(rotation=0)
    st.pyplot(fig)

    # --- Save chart to temporary PNG file ---
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight')
        tmpfile_path = tmpfile.name

    # --- PDF generation ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,f"{disease_selected} vs ICU Admission Report", ln=True, align="C")
    pdf.ln(5)

    # Insert chart
    chart_y = 25
    pdf.image(tmpfile_path, x=15, y=chart_y, w=180)

    # Dynamically set table starting below chart
    chart_height_mm = 100  # approximate chart height
    pdf.set_y(chart_y + chart_height_mm + 10)  # add margin after chart

    # Table header
    pdf.set_font("Arial","B",12)
    pdf.cell(60,10,disease_selected,1)
    pdf.cell(60,10,"ICU YES",1)
    pdf.cell(60,10,"ICU NO",1)
    pdf.ln()

    # Table rows
    pdf.set_font("Arial","",12)
    for i,row in cross_tab.iterrows():
        pdf.cell(60,10,str(row.name),1)
        pdf.cell(60,10,str(row.get("YES",0)),1)
        pdf.cell(60,10,str(row.get("NO",0)),1)
        pdf.ln()

    # Output PDF bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Download button
    st.download_button(
        label=f"Download {disease_selected} vs ICU PDF (With Chart)",
        data=pdf_bytes,
        file_name=f"{disease_selected}_icu_report.pdf",
        mime="application/pdf"
    )
