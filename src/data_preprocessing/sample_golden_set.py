import pandas as pd

INPUT_PATH = "data/amazon_conversations_clean.csv"
OUTPUT_PATH = "data/golden_set.csv"

df = pd.read_csv(INPUT_PATH)

# Sample complete conversations
sample = df.sample(
    n=200,
    random_state=42
).copy()

# Columns we will manually fill
sample["intent"] = ""
sample["expected_response"] = ""
sample["should_escalate"] = ""
sample["escalation_reason"] = ""

sample = sample[
    [
        "conversation_id",
        "num_messages",
        "conversation",
        "intent",
        "expected_response",
        "should_escalate",
        "escalation_reason",
    ]
]

sample.to_csv(OUTPUT_PATH, index=False)

print(f"Created golden set with {len(sample)} conversations")
print(f"Saved to: {OUTPUT_PATH}")