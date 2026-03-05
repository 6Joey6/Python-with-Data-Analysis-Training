import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
from utils import load_data
import io
import tempfile

st.set_page_config(page_title="Q2: Gender & Age Distribution")
st.title("Q2: Distribution of Cases by Gender & Age Group")

# --- Load dataset ---
df = load_data()

# --- Keep only rows with AGE ---
df_filtered = df.dropna(subset=["AGE"])

# --- Create AGE_GROUP with readable labels ---
bins = [0,10,20,30,40,50,60,70,80,90,100]
labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
df_filtered["AGE_GROUP"] = pd.cut(df_filtered["AGE"], bins=bins, labels=labels, right=False)

# --- Group by SEX and AGE_GROUP ---
age_gender_counts = (
    df_filtered.groupby(["SEX","AGE_GROUP"])
    .size()
    .reset_index(name="Number of Patients")
)

# --- Interactive Plotly Sunburst Chart ---
fig = px.sunburst(
    age_gender_counts,
    path=["SEX","AGE_GROUP"],
    values="Number of Patients",
    title="Cases Distribution by Gender & Age Group"
)
st.plotly_chart(fig)

# --- Show Table ---
st.subheader("Cases by Gender and Age Group")
st.dataframe(age_gender_counts)

# ------------------- PDF Generation -------------------
def create_pdf_with_chart(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Cases by Gender & Age Group", ln=True, align="C")
    pdf.ln(5)

    # --- Matplotlib chart for PDF (stacked bar chart) ---
    pivot_df = df.pivot(index="AGE_GROUP", columns="SEX", values="Number of Patients").fillna(0)
    fig, ax = plt.subplots(figsize=(8,4))
    pivot_df.plot(kind="bar", stacked=True, ax=ax, color=["skyblue","salmon"])
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Patients")
    ax.set_title("Cases Distribution by Gender & Age Group")
    for i, age_group in enumerate(pivot_df.index):
        bottom = 0
        for sex in pivot_df.columns:
            val = pivot_df.loc[age_group, sex]
            if val > 0:
                ax.text(i, bottom + val/2, str(int(val)), ha='center', va='center', color="black")
                bottom += val
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart to temporary PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name, format="png", dpi=150)
        tmpfile_path = tmpfile.name

    # Insert chart into PDF
    chart_y = 25
    pdf.image(tmpfile_path, x=15, y=chart_y, w=180)

    # --- Table below chart ---
    chart_height_mm = 100
    pdf.set_y(chart_y + chart_height_mm + 10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 10, "SEX", 1)
    pdf.cell(60, 10, "AGE_GROUP", 1)
    pdf.cell(60, 10, "Number of Patients", 1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 12)
    for i, row in df.iterrows():
        pdf.cell(60, 10, str(row["SEX"]), 1)
        pdf.cell(60, 10, str(row["AGE_GROUP"]), 1)
        pdf.cell(60, 10, str(int(row["Number of Patients"])), 1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# Generate PDF and provide download button
pdf_bytes = create_pdf_with_chart(age_gender_counts)
st.download_button(
    label="Download PDF (With Chart)",
    data=pdf_bytes,
    file_name="q2_gender_age_report.pdf",
    mime="application/pdf"
)
