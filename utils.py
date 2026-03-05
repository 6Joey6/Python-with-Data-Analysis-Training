import pandas as pd
import os

def load_data():
    """Load dataset.csv and map codes to readable labels."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset.csv")

    df = pd.read_csv(file_path)

    # Map coded columns to readable labels
    mapping_dict = {
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
        "ANOTHER CASE": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
        "MIGRANT": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
        "ICU": {1:"YES", 2:"NO", 97:"DOES NOT APPLY", 98:"IGNORED", 99:"UNKNOWN"},
        "OUTCOME": {1:"POSITIVE", 2:"NEGATIVE", 3:"PENDING"},
        "NATIONALITY": {1:"MEXICAN", 2:"FOREIGN", 99:"UNKNOWN"}
    }

    for col, mapping in mapping_dict.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    return df
