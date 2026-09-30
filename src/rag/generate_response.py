from .retriever import ConversationRetriever
from .build_context import build_context
from src.models.llm import call_llm

retriever = ConversationRetriever(top_k=3)


def generate_response(customer_message):

    results = retriever.retrieve(customer_message)

    context = build_context(results)

    prompt = f"""
You are an Amazon customer support assistant.

Generate a helpful response to the customer.

Use the historical AmazonHelp responses below as guidance.
Do not invent policies, refunds, delivery dates, or guarantees.
If the historical examples suggest that more information is needed,
ask the customer for it.

Historical examples:
{context}

Customer message:
{customer_message}

Write only the customer-facing response.
"""

    response = call_llm(prompt)

    return response


if __name__ == "__main__":

    customer_message = (
        "My package was supposed to arrive yesterday "
        "but still hasn't arrived."
    )

    response = generate_response(customer_message)

    print("\n=== GENERATED RESPONSE ===")
    print(response)