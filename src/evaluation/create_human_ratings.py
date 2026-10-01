import pandas as pd

INPUT_PATH = "data/response_judge_results.csv"
OUTPUT_PATH = "data/human_ratings.csv"

df = pd.read_csv(INPUT_PATH)

human_df = df[
    ["customer_message", "generated_response"]
].copy()

human_df["human_relevance"] = ""
human_df["human_groundedness"] = ""
human_df["human_helpfulness"] = ""
human_df["human_reason"] = ""

human_df.to_csv(OUTPUT_PATH, index=False)

print(f"Created {OUTPUT_PATH}")
print(f"Responses to rate: {len(human_df)}")