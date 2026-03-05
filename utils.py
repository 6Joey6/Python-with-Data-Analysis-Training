import pandas as pd

def load_data():

    df = pd.read_csv("covid_data.csv")

    # Mapping values
    df["SEX"] = df["SEX"].map({
        1:"FEMALE",
        2:"MALE",
        99:"UNKNOWN"
    })

    df["HOSPITALIZED"] = df["HOSPITALIZED"].map({
        1:"YES",
        2:"NO",
        99:"UNKNOWN"
    })

    return df


def create_age_group(df):

    bins = [0,10,20,30,40,50,60,70,80,90,100]

    df["AGE_GROUP"] = pd.cut(
        df["AGE"],
        bins=bins
    )

    return df
