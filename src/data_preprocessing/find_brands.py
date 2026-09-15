import pandas as pd


DATA_PATH = "data/twcs.csv"

df = pd.read_csv(DATA_PATH)

brands = (
    df[df["inbound"] == False]["author_id"]
    .value_counts()
    .head(30)
)

print("Top 30 possible brands:\n")
print(brands)