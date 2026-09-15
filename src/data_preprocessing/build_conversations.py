import pandas as pd


DATA_PATH = "data/amazon_help.csv"
OUTPUT_PATH = "data/amazon_conversations.csv"


df = pd.read_csv(DATA_PATH)

tweet_map = df.set_index("tweet_id").to_dict("index")

# parent tweet -> all direct replies
children_map = {}

for _, row in df[df["in_response_to_tweet_id"].notna()].iterrows():
    parent_id = int(row["in_response_to_tweet_id"])
    children_map.setdefault(parent_id, []).append(int(row["tweet_id"]))


def find_root(tweet_id):
    visited = set()
    current_id = tweet_id

    while current_id in tweet_map and current_id not in visited:
        visited.add(current_id)

        parent_id = tweet_map[current_id]["in_response_to_tweet_id"]

        if pd.isna(parent_id):
            break

        parent_id = int(parent_id)

        if parent_id not in tweet_map:
            break

        current_id = parent_id

    return current_id


def collect_thread(root_id):
    """Collect every tweet reachable from the root."""

    collected = []
    stack = [root_id]
    visited = set()

    while stack:
        current_id = stack.pop()

        if current_id in visited or current_id not in tweet_map:
            continue

        visited.add(current_id)

        tweet = tweet_map[current_id]

        collected.append({
            "tweet_id": current_id,
            "author_id": tweet["author_id"],
            "inbound": tweet["inbound"],
            "created_at": tweet["created_at"],
            "text": tweet["text"],
        })

        # Add all replies
        for child_id in children_map.get(current_id, []):
            stack.append(child_id)

    # Chronological order
    collected.sort(key=lambda x: x["created_at"])

    return collected


# Find unique conversation roots
roots = set()

for tweet_id in df["tweet_id"]:
    roots.add(find_root(tweet_id))

print("Unique conversation roots:", len(roots))


conversations = []

for conversation_id, root_id in enumerate(roots):

    thread = collect_thread(root_id)

    if len(thread) < 2:
        continue

    conversations.append({
        "conversation_id": conversation_id,
        "num_messages": len(thread),
        "conversation": "\n".join(
            f"{'CUSTOMER' if msg['inbound'] else 'AMAZONHELP'}: {msg['text']}"
            for msg in thread
        )
    })


result = pd.DataFrame(conversations)

result.to_csv(OUTPUT_PATH, index=False)

print("Unique conversations:", len(result))
print("Saved to:", OUTPUT_PATH)

print("\nFirst 5 conversations:")

for i in range(min(5, len(result))):
    print(f"\n--- Conversation {i} ---")
    print(result.iloc[i]["conversation"])