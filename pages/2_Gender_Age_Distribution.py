# Filter only meaningful SEX and AGE
df_filtered = df[df["SEX"].isin(["FEMALE","MALE"])]
df_filtered = df_filtered.dropna(subset=["AGE"])
df_filtered["AGE_GROUP"] = pd.cut(df_filtered["AGE"], bins=[0,10,20,30,40,50,60,70,80,90,100])

# Use df_filtered for chart & download
