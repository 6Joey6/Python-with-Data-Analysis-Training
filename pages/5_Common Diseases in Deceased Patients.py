import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

    disease_counts = {d: (df_deceased[d] == "YES").sum() for d in diseases}
    disease_df = pd.DataFrame(list(disease_counts.items()), columns=["Disease", "Number of Deceased Patients"])

    if disease_df["Number of Deceased Patients"].sum() == 0:
        st.warning("No disease information available for deceased patients.")
    else:
        # --- Create matplotlib chart instead of Plotly ---
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(disease_df["Disease"], disease_df["Number of Deceased Patients"], color="skyblue")
        ax.set_title("Common Diseases Among Deceased Patients")
        ax.set_ylabel("Number of Deceased Patients")
        ax.set_xlabel("Disease")
        for i, v in enumerate(disease_df["Number of Deceased Patients"]):
            ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        st.dataframe(disease_df)

        # --- PDF generation ---
        def create_pdf_with_chart(df, fig):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "Deceased Patients Disease Report", ln=True, align="C")
            pdf.ln(5)

            # Save matplotlib figure to temp PNG
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                fig.savefig(tmpfile.name, format="png", dpi=150)
                tmpfile_path = tmpfile.name

            # Insert chart
            chart_y = 25
            pdf.image(tmpfile_path, x=15, y=chart_y, w=180)

            # Table below chart
            chart_height_mm = 100
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

        pdf_bytes = create_pdf_with_chart(disease_df, fig)

        st.download_button(
            label="Download PDF (With Chart)",
            data=pdf_bytes,
            file_name="deceased_disease_report_with_chart.pdf",
            mime="application/pdf"
        )
