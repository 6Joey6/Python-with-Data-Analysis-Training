import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data
from fpdf import FPDF
import io

# Page setup
st.set_page_config(page_title="Q4: Disease vs ICU Admission")
st.title("Q4: Correlation Between Diseases and ICU Admission")

# Load data
df = load_data()

diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
            "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
            "CHRONIC_KIDNEY", "TOBACCO"]

disease_selected = st.selectbox("Select a Disease", diseases)

df_filtered = df[df["ICU"].isin(["YES","NO"]) & df[disease_selected].isin(["YES","NO"])]

if df_filtered.empty:
    st.warning(f"No data available for {disease_selected} vs ICU.")
else:
    cross_tab = pd.crosstab(df_filtered[disease_selected], df_filtered["ICU"])
    st.subheader(f"ICU Admission vs {disease_selected}")
    st.dataframe(cross_tab)

    # --- Matplotlib chart ---
    fig, ax = plt.subplots()
    cross_tab.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel(disease_selected)
    ax.set_ylabel("Number of Patients")
    ax.set_title(f"{disease_selected} vs ICU Admission")
    plt.xticks(rotation=0)
    st.pyplot(fig)

    # Save chart to PNG in memory
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    chart_bytes = buf.read()

    # --- PDF generation ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,f"{disease_selected} vs ICU Admission Report", ln=True, align="C")
    pdf.ln(5)

    # Insert chart
    tmp_img = io.BytesIO(chart_bytes)
    pdf.image(tmp_img, x=15, y=25, w=180)
    pdf.ln(125)

    # Table
    pdf.set_font("Arial","B",12)
    pdf.cell(60,10,disease_selected,1)
    pdf.cell(60,10,"ICU YES",1)
    pdf.cell(60,10,"ICU NO",1)
    pdf.ln()
    pdf.set_font("Arial","",12)
    for i,row in cross_tab.iterrows():
        pdf.cell(60,10,str(row.name),1)
        pdf.cell(60,10,str(row.get("YES",0)),1)
        pdf.cell(60,10,str(row.get("NO",0)),1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')

    st.download_button(
        label=f"Download {disease_selected} vs ICU PDF (With Chart)",
        data=pdf_bytes,
        file_name=f"{disease_selected}_icu_report.pdf",
        mime="application/pdf"
    )
