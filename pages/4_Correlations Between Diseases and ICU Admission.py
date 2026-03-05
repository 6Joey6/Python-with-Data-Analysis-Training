import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from fpdf import FPDF

st.set_page_config(page_title="Q4: Disease vs ICU Admission")
st.title("Q4: Correlation Between Diseases and ICU Admission")

df = load_data()

# List of diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Select disease to analyze
disease_selected = st.selectbox("Select a Disease", diseases)

# Filter for rows where ICU and disease are YES/NO
df_filtered = df[
    df["ICU"].isin(["YES","NO"]) & df[disease_selected].isin(["YES","NO"])
]

if df_filtered.empty:
    st.warning(f"No data available for {disease_selected} vs ICU in this dataset.")
else:
    # Cross-tab
    cross_tab = pd.crosstab(df_filtered[disease_selected], df_filtered["ICU"])

    st.subheader(f"ICU Admission vs {disease_selected}")
    st.dataframe(cross_tab)

    # Plot stacked bar chart
    fig = px.bar(
        cross_tab,
        x=cross_tab.index,
        y=["YES","NO"],
        title=f"{disease_selected} vs ICU Admission",
        labels={"value":"Number of Patients", "x":disease_selected},
        text_auto=True
    )
    st.plotly_chart(fig)

    # PDF download
    def create_pdf(df, disease):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{disease} vs ICU Admission Report", ln=True, align="C")
        pdf.ln(5)
        # Header
        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 10, disease, 1)
        pdf.cell(60, 10, "ICU YES", 1)
        pdf.cell(60, 10, "ICU NO", 1)
        pdf.ln()
        # Rows
        pdf.set_font("Arial", "", 12)
        for i, row in df.iterrows():
            pdf.cell(60, 10, str(row.name), 1)
            pdf.cell(60, 10, str(row.get("YES",0)), 1)
            pdf.cell(60, 10, str(row.get("NO",0)), 1)
            pdf.ln()
        # Return PDF as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        return pdf_bytes

    pdf_bytes = create_pdf(cross_tab, disease_selected)
    st.download_button(
        label=f"Download {disease_selected} vs ICU PDF",
        data=pdf_bytes,
        file_name=f"{disease_selected}_icu_report.pdf",
        mime="application/pdf"
    )
