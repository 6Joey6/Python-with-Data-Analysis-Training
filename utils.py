# utils.py
import pandas as pd
import os

# Mapping dictionaries based on your data_dictionary.csv
MAPPINGS = {
    "SEX": {1:"FEMALE", 2:"MALE", 99:"UNKNOWN"},
    "HOSPITALIZED": {1:"NO", 2:"YES", 99:"UNKNOWN"},
    "INTUBATED": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "PNEUMONIA": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "PREGNANCY": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "SPEAKS_NATIVE_LANGUAGE": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "DIABETES": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "COPD": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "ASTHMA": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "INMUSUPR": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "HYPERTENSION": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "OTHER_DISEASE": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "CARDIOVASCULAR": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "OBESITY": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "CHRONIC_KIDNEY": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "TOBACCO": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "ANOTHER_CASE": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "MIGRANT": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "ICU": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
    "OUTCOME": {1:"POSITIVE", 2:"NEGATIVE", 3:"PENDING"},
    "NATIONALITY": {1:"MEXICAN", 2:"FOREIGN", 99:"UNKNOWN"}
}

# Columns that should be numeric for analysis
NUMERIC_COLS = [
    "AGE",
    "ICU","DIABETES","COPD","ASTHMA","INMUSUPR",
    "HYPERTENSION","CARDIOVASCULAR","OBESITY","CHRONIC_KIDNEY","TOBACCO"
]

# Date columns
DATE_COLS = ["ADMISSION DATE", "DATE_OF_FIRST_SYMPTOM", "DATE_OF_DEATH"]

def load_data():
    """
    Load dataset.csv, map coded columns to readable values, convert numeric and date columns.
    Returns a cleaned pandas DataFrame.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset.csv")
    df = pd.read_csv(file_path)

    # Map coded columns
    for col, mapping in MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # Convert numeric columns
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert date columns
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    return df

