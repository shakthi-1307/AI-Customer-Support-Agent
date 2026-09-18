import pandas as pd

INPUT_PATH = "data/golden_set.csv"
OUTPUT_PATH = "data/golden_set.csv"

df = pd.read_csv(INPUT_PATH)
df["intent"] = df["intent"].fillna("")
df["expected_response"] = df["expected_response"].fillna("")
df["should_escalate"] = df["should_escalate"].fillna("")
df["escalation_reason"] = df["escalation_reason"].fillna("")

intents = [
    "Delivery / Tracking",
    "Order / Pricing",
    "Return / Replacement",
    "Refund",
    "Payment / Billing",
    "Account / Login",
    "Prime Membership",
    "Product / Device",
    "Digital Content",
    "Security / Fraud",
    "Customer Service / Complaint",
    "Other",
]

for i in range(len(df)):

    # Skip already labelled rows
    if pd.notna(df.loc[i, "intent"]) and str(df.loc[i, "intent"]).strip():
        continue

    print("\n" + "=" * 80)
    print(f"CASE {i + 1} / {len(df)}")
    print("=" * 80)

    print(df.loc[i, "conversation"])

    print("\nINTENTS:")
    for j, intent in enumerate(intents, 1):
        print(f"{j}. {intent}")

    while True:
        choice = input("\nChoose intent number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(intents):
            intent = intents[int(choice) - 1]
            break

        print("Invalid choice.")

    escalate = input("Should escalate? (y/n): ").strip().lower()

    if escalate == "y":
        should_escalate = True
        reason = input("Escalation reason: ").strip()
    else:
        should_escalate = False
        reason = ""

    df.loc[i, "intent"] = intent
    df.loc[i, "should_escalate"] = should_escalate
    df.loc[i, "escalation_reason"] = reason

    # Save after every case
    df.to_csv(OUTPUT_PATH, index=False)

    print("Saved.")

print("\nGolden-set labeling complete.")