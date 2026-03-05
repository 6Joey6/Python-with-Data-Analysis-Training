import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from fpdf import FPDF

st.title("Q4: Correlation Between Diseases and ICU Admission")

df = load_data()

# Diseases
diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

disease_selected = st.selectbox("Select a Disease", diseases)

df_filtered = df[df["ICU"].isin(["YES","NO"]) & df[disease_selected].isin(["YES","NO"])]

if df_filtered.empty:
    st.warning(f"No data for {disease_selected} vs ICU.")
else:
    cross_tab = pd.crosstab(df_filtered[disease_selected], df_filtered["ICU"])

    # Melt for Plotly
    cross_tab_long = cross_tab.reset_index().melt(id_vars=disease_selected,
                                                  value_vars=["YES","NO"],
                                                  var_name="ICU",
                                                  value_name="Number of Patients")

    st.dataframe(cross_tab)

    # Plot
    fig = px.bar(
        cross_tab_long,
        x=disease_selected,
        y="Number of Patients",
        color="ICU",
        text="Number of Patients",
        title=f"{disease_selected} vs ICU Admission"
    )
    st.plotly_chart(fig)

    # PDF
    def create_pdf(df, disease):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,f"{disease} vs ICU Report", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial","B",12)
        pdf.cell(60,10,disease,1)
        pdf.cell(60,10,"ICU YES",1)
        pdf.cell(60,10,"ICU NO",1)
        pdf.ln()
        pdf.set_font("Arial","",12)
        for i,row in df.iterrows():
            pdf.cell(60,10,str(row.name),1)
            pdf.cell(60,10,str(row.get("YES",0)),1)
            pdf.cell(60,10,str(row.get("NO",0)),1)
            pdf.ln()
        return pdf.output(dest='S').encode('latin1')

    pdf_bytes = create_pdf(cross_tab, disease_selected)
    st.download_button(
        "Download PDF",
        data=pdf_bytes,
        file_name=f"{disease_selected}_icu_report.pdf",
        mime="application/pdf"
    )
