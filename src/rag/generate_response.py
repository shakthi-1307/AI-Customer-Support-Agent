import pandas as pd

from .retriever import ConversationRetriever
from .build_context import build_context
from src.models.llm import call_llm


GOLDEN_PATH = "data/golden_set.csv"

retriever = ConversationRetriever(top_k=3)


def generate_response(customer_message):
    results = retriever.retrieve(customer_message)
    context = build_context(results)

    prompt = f"""
You are an Amazon customer support agent.

Customer message:
{customer_message}

Historical support examples:
{context}

Write a helpful reply to the customer.

Rules:
1. Directly address the customer's message.
2. Use the historical examples only as guidance.
3. Do not invent order details, tracking information, refunds, links, or actions.
4. Do not claim that you contacted the customer through DM or another channel.
5. If the historical examples do not contain enough information, give a safe general response.
6. Write only the customer-facing reply.
7. Keep it concise and complete.
8. Never use "here", "below", "this link", or "click here" unless an actual link is provided.
9. Do not mention links if no usable link is available.
"""

    response = call_llm(prompt)

    response = response.replace("[Link to Return/Replacement Options]", "")
    response = response.replace("[Link]", "")

    return response.strip()

if __name__ == "__main__":

    df = pd.read_csv(GOLDEN_PATH)

    for i, row in df.head(5).iterrows():

        customer_message = row["conversation"]

        # Get the latest customer message
        messages = customer_message.split("\n")

        customer_messages = [
            msg.replace("CUSTOMER:", "", 1).strip()
            for msg in messages
            if msg.startswith("CUSTOMER:")
        ]

        if not customer_messages:
            continue

        customer_message = customer_messages[-1]

        print(f"\n{'=' * 60}")
        print(f"Example {i + 1}")
        print(f"Customer: {customer_message}")

        response = generate_response(customer_message)

        print(f"Generated: {response}")