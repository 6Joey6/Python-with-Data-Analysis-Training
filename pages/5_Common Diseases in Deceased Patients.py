import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from utils import load_data
import io

st.title("Q5: Common Diseases Among Deceased Patients")

# Load dataset
df = load_data()

# Keep only deceased patients
df_deceased = df[df["DATE_OF_DEATH"].notna()]

if df_deceased.empty:
    st.warning("No deceased patient data available in this dataset.")
else:
    diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR",
                "HYPERTENSION", "CARDIOVASCULAR", "OBESITY",
                "CHRONIC_KIDNEY", "TOBACCO"]

    # Count YES for each disease
    disease_counts = {d: (df_deceased[d] == "YES").sum() for d in diseases}
    disease_df = pd.DataFrame(list(disease_counts.items()), columns=["Disease", "Number of Deceased Patients"])

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
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "Deceased Patients Disease Report", ln=True, align="C")
            pdf.ln(5)

            # Export Plotly figure to PNG in-memory
            img_bytes = fig.to_image(format="png", width=800, height=400, engine="kaleido")
            img_buffer = io.BytesIO(img_bytes)

            # Save PNG temporarily in /tmp (safe on Streamlit Cloud)
            tmp_path = "/tmp/chart.png"
            with open(tmp_path, "wb") as f:
                f.write(img_buffer.getvalue())

            # Insert chart into PDF
            chart_y = 25
            pdf.image(tmp_path, x=15, y=chart_y, w=180)

            # Table below chart
            chart_height_mm = 100  # approximate chart height
            pdf.set_y(chart_y + chart_height_mm + 10)

            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(80, 10, "Disease", 1)
            pdf.cell(80, 10, "Number of Deceased Patients", 1)
            pdf.ln()

            pdf.set_font("Helvetica", "", 12)
            for i, row in df.iterrows():
                pdf.cell(80, 10, str(row["Disease"]), 1)
                pdf.cell(80, 10, str(row["Number of Deceased Patients"]), 1)
                pdf.ln()

            pdf_bytes = pdf.output(dest='S').encode('latin1')
            return pdf_bytes

        # Generate PDF
        pdf_bytes = create_pdf_with_chart(disease_df, fig)

        # Download button
        st.download_button(
            label="Download PDF (With Chart)",
            data=pdf_bytes,
            file_name="deceased_disease_report_with_chart.pdf",
            mime="application/pdf"
        )
