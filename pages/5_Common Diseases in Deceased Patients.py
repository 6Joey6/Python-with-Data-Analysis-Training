import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from utils import load_data
import tempfile

st.title("Q5: Common Diseases Among Deceased Patients")

df = load_data()

df_deceased = df[df["DATE_OF_DEATH"].notna()]

if df_deceased.empty:
    st.warning("No deceased patient data available in this dataset.")
else:
    diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
                "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
                "CHRONIC_KIDNEY", "TOBACCO"]

    disease_counts = {}
    for disease in diseases:
        disease_counts[disease] = (df_deceased[disease] == "YES").sum()

    disease_df = pd.DataFrame(list(disease_counts.items()), columns=["Disease","Number of Deceased Patients"])

    if disease_df["Number of Deceased Patients"].sum() == 0:
        st.warning("No disease information available for deceased patients.")
    else:
        # Plot chart
        fig = px.bar(
            disease_df,
            x="Disease",
            y="Number of Deceased Patients",
            title="Common Diseases Among Deceased Patients",
            text_auto=True
        )
        st.plotly_chart(fig)
        st.dataframe(disease_df)

        # --- PDF generation with chart ---
        def create_pdf_with_chart(df, fig):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Deceased Patients Disease Report", ln=True, align="C")
            pdf.ln(5)

            # Save Plotly figure to a temporary PNG
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                fig.write_image(tmpfile.name, width=800, height=400)
                tmpfile_path = tmpfile.name

            # Insert chart
            chart_y = 25
            pdf.image(tmpfile_path, x=15, y=chart_y, w=180)

            # Table below chart
            chart_height_mm = 100  # approximate height
            pdf.set_y(chart_y + chart_height_mm + 10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(80, 10, "Disease", 1)
            pdf.cell(80, 10, "Number of Deceased Patients", 1)
            pdf.ln()

            pdf.set_font("Arial", "", 12)
            for i, row in df.iterrows():
                pdf.cell(80, 10, str(row["Disease"]), 1)
                pdf.cell(80, 10, str(row["Number of Deceased Patients"]), 1)
                pdf.ln()

            pdf_bytes = pdf.output(dest='S').encode('latin1')
            return pdf_bytes

        pdf_bytes = create_pdf_with_chart(disease_df, fig)

        st.download_button(
            label="Download PDF (With Chart)",
            data=pdf_bytes,
            file_name="deceased_disease_report_with_chart.pdf",
            mime="application/pdf"
        )
