def load_data():
    import pandas as pd
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset.csv")

    df = pd.read_csv(file_path)

    # Convert columns to numeric if possible (ignore errors)
    numeric_cols = [
        "ICU","DIABETES","COPD","ASTHMA","INMUSUPR",
        "HYPERTENSION","CARDIOVASCULAR","OBESITY","CHRONIC_KIDNEY","TOBACCO"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
