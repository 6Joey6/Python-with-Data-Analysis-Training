# Only rows with YES/NO
intubated_df = df[df["INTUBATED"].isin(["YES","NO"])]
