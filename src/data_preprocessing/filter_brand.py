import pandas as pd


DATA_PATH = "data/twcs.csv"
OUTPUT_PATH = "data/amazon_help.csv"

df = pd.read_csv(DATA_PATH)

brand_df = df[
    (df["author_id"] == "AmazonHelp") |
    (df["text"].str.contains("@AmazonHelp", case=False, na=False))
].copy()

print("AmazonHelp tweets:", len(brand_df))
print("\nInbound:")
print(brand_df["inbound"].value_counts())

brand_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved to: {OUTPUT_PATH}")