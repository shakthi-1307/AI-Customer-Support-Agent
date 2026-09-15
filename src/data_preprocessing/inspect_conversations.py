import pandas as pd


DATA_PATH = "data/amazon_help.csv"

df = pd.read_csv(DATA_PATH)

# Keep only rows that have a known parent tweet
replies = df[df["in_response_to_tweet_id"].notna()].copy()

print("Total tweets:", len(df))
print("Tweets with parent:", len(replies))

print("\nSample reply relationships:\n")

print(
    replies[
        [
            "tweet_id",
            "author_id",
            "inbound",
            "text",
            "in_response_to_tweet_id",
        ]
    ].head(20).to_string(index=False)
)