from retriever import ConversationRetriever
from build_context import build_context


retriever = ConversationRetriever(top_k=3)

query = "My package was supposed to arrive yesterday but still hasn't arrived."

results = retriever.retrieve(query)

context = build_context(results)

print("\n=== RAG CONTEXT ===")
print(context)