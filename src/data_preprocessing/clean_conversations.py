import pandas as pd
import re
import html


INPUT_PATH = "data/amazon_conversations.csv"
OUTPUT_PATH = "data/amazon_conversations_clean.csv"


df = pd.read_csv(INPUT_PATH)


def clean_text(text):
    # Decode HTML entities
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove Twitter mentions
    text = re.sub(r"@\w+", "", text)

    # Remove agent signatures such as ^CR, ^AG
    text = re.sub(r"\^[A-Z]{1,3}\b", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_conversation(conversation):
    lines = conversation.split("\n")

    cleaned_lines = []

    for line in lines:

        if line.startswith("CUSTOMER:"):
            text = line.replace("CUSTOMER:", "", 1).strip()
            text = clean_text(text)

            if text:
                cleaned_lines.append(f"CUSTOMER: {text}")

        elif line.startswith("AMAZONHELP:"):
            text = line.replace("AMAZONHELP:", "", 1).strip()
            text = clean_text(text)

            if text:
                cleaned_lines.append(f"AMAZONHELP: {text}")

    return "\n".join(cleaned_lines)


df["conversation"] = df["conversation"].apply(clean_conversation)

# Remove conversations that became empty or have fewer than 2 messages
df = df[df["conversation"].str.strip() != ""]

df.to_csv(OUTPUT_PATH, index=False)

print("Clean conversations:", len(df))
print("Saved to:", OUTPUT_PATH)

print("\nExamples:")

for i in range(min(5, len(df))):
    print(f"\n--- Conversation {i} ---")
    print(df.iloc[i]["conversation"])