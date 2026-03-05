import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from fpdf import FPDF

# Page setup
st.set_page_config(page_title="Q4: Disease vs ICU Admission")
st.title("Q4: Correlation Between Diseases and ICU Admission")

# --- Load dataset ---
df = load_data()

# --- List of diseases to analyze ---
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

# Disease selection UI
disease_selected = st.selectbox("Select a Disease", diseases)

# Filter rows with valid ICU and disease values
df_filtered = df[df["ICU"].isin(["YES","NO"]) & df[disease_selected].isin(["YES","NO"])]

if df_filtered.empty:
    st.warning(f"No data available for {disease_selected} vs ICU.")
else:
    # Create crosstab
    cross_tab = pd.crosstab(df_filtered[disease_selected], df_filtered["ICU"])

    # Melt for Plotly chart
    cross_tab_long = cross_tab.reset_index().melt(
        id_vars=disease_selected,
        value_vars=["YES","NO"],
        var_name="ICU",
        value_name="Number of Patients"
    )

    # Display table in Streamlit
    st.subheader(f"ICU Admission vs {disease_selected}")
    st.dataframe(cross_tab)

    # Plot interactive bar chart
    fig = px.bar(
        cross_tab_long,
        x=disease_selected,
        y="Number of Patients",
        color="ICU",
        text="Number of Patients",
        title=f"{disease_selected} vs ICU Admission"
    )
    st.plotly_chart(fig)

    # PDF generation (table only)
    def create_pdf(df_table, disease):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,f"{disease} vs ICU Admission Report", ln=True, align="C")
        pdf.ln(5)

        # Table header
        pdf.set_font("Arial","B",12)
        pdf.cell(60,10,disease,1)
        pdf.cell(60,10,"ICU YES",1)
        pdf.cell(60,10,"ICU NO",1)
        pdf.ln()

        # Table rows
        pdf.set_font("Arial","",12)
        for i,row in df_table.iterrows():
            pdf.cell(60,10,str(row.name),1)
            pdf.cell(60,10,str(row.get("YES",0)),1)
            pdf.cell(60,10,str(row.get("NO",0)),1)
            pdf.ln()

        pdf_bytes = pdf.output(dest='S').encode('latin1')
        return pdf_bytes

    pdf_bytes = create_pdf(cross_tab, disease_selected)

    # Download button
    st.download_button(
        label=f"Download {disease_selected} vs ICU PDF (Table Only)",
        data=pdf_bytes,
        file_name=f"{disease_selected}_icu_report.pdf",
        mime="application/pdf"
    )
