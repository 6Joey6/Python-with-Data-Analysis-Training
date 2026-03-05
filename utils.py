import pandas as pd
import os

def load_data():
    """Load dataset.csv and ensure numeric columns are numeric"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset.csv")

    df = pd.read_csv(file_path)

    # Columns to convert to numeric
    numeric_cols = [
        "ICU","DIABETES","COPD","ASTHMA","INMUSUPR",
        "HYPERTENSION","CARDIOVASCULAR","OBESITY","CHRONIC_KIDNEY","TOBACCO"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # convert errors to NaN

    return df
