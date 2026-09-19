import pandas as pd

PATH = "data/golden_set.csv"

df = pd.read_csv(PATH)

print("Total:", len(df))

print("\n=== INTENT DISTRIBUTION ===")
print(df["intent"].value_counts())

print("\n=== ESCALATION DISTRIBUTION ===")
print(df["should_escalate"].value_counts())

print("\n=== MISSING VALUES ===")
print(df[["intent", "should_escalate", "escalation_reason"]].isna().sum())

print("\n=== EXPECTED RESPONSE ===")
print("Filled:", df["expected_response"].notna().sum())
print("Empty:", df["expected_response"].isna().sum())