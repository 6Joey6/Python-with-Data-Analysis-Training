import pandas as pd

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

def load_data():
    df = pd.read_csv("dataset.csv")

    # Convert AGE to numeric
    df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce")

    # Convert dates
    df["ADMISSION DATE"] = pd.to_datetime(df["ADMISSION DATE"], errors="coerce", dayfirst=True)
    df["DATE_OF_FIRST_SYMPTOM"] = pd.to_datetime(df["DATE_OF_FIRST_SYMPTOM"], errors="coerce", dayfirst=True)
    df["DATE_OF_DEATH"] = pd.to_datetime(df["DATE_OF_DEATH"], errors="coerce", dayfirst=True)

    # Map values
    for col, mapping in MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    return df
