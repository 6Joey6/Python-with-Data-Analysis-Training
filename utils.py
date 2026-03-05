# utils.py
import pandas as pd
import os

def load_data():
    """Load dataset.csv and map coded columns according to data_dictionary.csv"""
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load dataset
    dataset_path = os.path.join(BASE_DIR, "dataset.csv")
    df = pd.read_csv(dataset_path)

    # Load data dictionary
    dict_path = os.path.join(BASE_DIR, "data_dictionary.csv")
    data_dict = pd.read_csv(dict_path)

    # Mapping for each column according to data dictionary
    mapping_columns = [
        "SEX","HOSPITALIZED","INTUBATED","PNEUMONIA","PREGNANCY",
        "SPEAKS_NATIVE_LANGUAGE","DIABETES","COPD","ASTHMA","INMUSUPR",
        "HYPERTENSION","OTHER_DISEASE","CARDIOVASCULAR","OBESITY",
        "CHRONIC_KIDNEY","TOBACCO","ANOTHER CASE","MIGRANT","ICU",
        "OUTCOME","NATIONALITY"
    ]

    for col in mapping_columns:
        # Find the mapping row in data_dictionary
        row = data_dict[data_dict['variable'] == col]
        if not row.empty:
            value_str = row['value'].values[0]  # e.g., "1 = Female, 2 = Male, 99 = Unknown"
            # Build a dict: {1:"FEMALE", 2:"MALE", 99:"UNKNOWN"}
            mapping = {}
            for part in value_str.split(','):
                if '=' in part:
                    k, v = part.split('=')
                    k = k.strip()
                    v = v.strip()
                    # convert numeric key if possible
                    try:
                        k = int(k)
                    except:
                        pass
                    mapping[k] = v.upper()  # convert values to uppercase for consistency
            # Apply mapping
            if col in df.columns:
                df[col] = df[col].map(mapping)

    return df
