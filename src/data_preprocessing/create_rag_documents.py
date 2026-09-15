import pandas as pd
import json


INPUT_PATH = "data/amazon_conversations_clean.csv"
OUTPUT_PATH = "data/amazon_rag_documents.jsonl"


df = pd.read_csv(INPUT_PATH)


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:

    for _, row in df.iterrows():

        document = {
            "conversation_id": int(row["conversation_id"]),
            "num_messages": int(row["num_messages"]),
            "text": row["conversation"]
        }

        f.write(json.dumps(document, ensure_ascii=False) + "\n")


print(f"Created {len(df)} RAG documents")
print(f"Saved to: {OUTPUT_PATH}")
