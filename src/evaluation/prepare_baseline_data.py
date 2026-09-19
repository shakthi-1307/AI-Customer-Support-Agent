import pandas as pd

INPUT_PATH = "data/golden_set.csv"
OUTPUT_PATH = "data/baseline_data.csv"

df = pd.read_csv(INPUT_PATH)

def get_latest_customer_message(conversation):
    messages = conversation.split("\n")

    customer_messages = [
        msg.replace("CUSTOMER:", "", 1).strip()
        for msg in messages
        if msg.startswith("CUSTOMER:")
    ]

    return customer_messages[-1] if customer_messages else ""

df["input_text"] = df["conversation"].apply(get_latest_customer_message)

result = df[
    [
        "conversation_id",
        "input_text",
        "intent",
        "should_escalate",
        "escalation_reason",
        "conversation"
    ]
]

result.to_csv(OUTPUT_PATH, index=False)

print(f"Created: {OUTPUT_PATH}")
print(f"Rows: {len(result)}")

print("\nExamples:")
print(result[["input_text", "intent"]].head(10).to_string(index=False))