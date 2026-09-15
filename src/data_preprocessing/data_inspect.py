import pandas as pd


DATA_PATH = "data/twcs.csv"


df = pd.read_csv(DATA_PATH)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nNumber of authors:", df["author_id"].nunique())

print("\nInbound distribution:")
print(df["inbound"].value_counts())

print("\nSample:")
print(df.head())