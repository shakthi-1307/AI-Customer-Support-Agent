from retriever import ConversationRetriever


retriever = ConversationRetriever(top_k=3)

query = "My package was supposed to arrive yesterday but still hasn't arrived."

results = retriever.retrieve(query)

for i, result in enumerate(results, 1):
    print(f"\n=== RESULT {i} ===")
    print("Score:", result["score"])
    print("Conversation ID:", result["conversation_id"])
    print(result["conversation"])