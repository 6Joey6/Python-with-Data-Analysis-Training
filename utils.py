# utils.py
import pandas as pd
import os

def load_data():
    """Load dataset.csv and convert important columns to numeric"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset.csv")

    df = pd.read_csv(file_path)

    # Columns to convert
    numeric_cols = [
        "ICU","INTUBATED","DIABETES","COPD","ASTHMA","INMUSUPR",
        "HYPERTENSION","CARDIOVASCULAR","OBESITY","CHRONIC_KIDNEY","TOBACCO",
        "HOSPITALIZED","PNEUMONIA","PREGNANCY","ANOTHER CASE"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # convert errors to NaN

    return df
