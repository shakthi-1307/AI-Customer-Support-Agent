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
You are an Amazon customer support assistant.

Generate a helpful response to the customer.

Use the historical AmazonHelp responses as guidance.
Do not invent policies, refunds, delivery dates, or guarantees.
If more information is needed, ask the customer for it.

Historical examples:
{context}

Customer message:
{customer_message}

Write only the customer-facing response.
"""

    return call_llm(prompt)


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