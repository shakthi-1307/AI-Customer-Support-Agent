import pandas as pd

df = pd.read_csv("data/agent_evaluation_results.csv")

missed = df[
    (df["should_escalate"] == True)
    & (df["predicted_escalation"] == False)
]

print("Missed escalation cases:", len(missed))

for _, row in missed.iterrows():
    print("\n" + "=" * 60)
    print("Conversation ID:", row["conversation_id"])
    print("Conversation:")
    print(row["conversation"])