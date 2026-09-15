import pandas as pd


INPUT_PATH = "data/amazon_conversations_clean.csv"

df = pd.read_csv(INPUT_PATH)


customer_messages = []

for _, row in df.iterrows():
    lines = row["conversation"].split("\n")

    for line in lines:
        if line.startswith("CUSTOMER:"):
            text = line.replace("CUSTOMER:", "", 1).strip()

            if text:
                customer_messages.append(text)


print("Total customer messages:", len(customer_messages))

print("\nSample customer messages:\n")

for i, message in enumerate(customer_messages[:50]):
    print(f"{i + 1}. {message}")
    
import random

random.seed(42)

sample = random.sample(
    customer_messages,
    min(200, len(customer_messages))
)

print("\nRandom sample:\n")

for i, message in enumerate(sample):
    print(f"{i + 1}. {message}")