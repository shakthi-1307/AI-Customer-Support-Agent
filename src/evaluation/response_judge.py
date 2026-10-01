import json
import pandas as pd

from src.models.llm import call_llm
from src.rag.generate_response import generate_response


INPUT_PATH = "data/agent_evaluation_results.csv"
OUTPUT_PATH = "data/response_judge_results.csv"


def judge_response(customer_message, generated_response):
    prompt = f"""
You are evaluating an AI customer support response.

Rate the response on these dimensions from 1 to 5:
- Relevance: Does it address the customer's issue?
- Groundedness: Does it avoid unsupported claims or promises?
- Helpfulness: Does it provide a useful next step?

Return only valid JSON:
{{
    "relevance": 1,
    "groundedness": 1,
    "helpfulness": 1,
    "reason": "Brief explanation"
}}

Customer message:
{customer_message}

Generated response:
{generated_response}
"""

    result = call_llm(prompt)

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "relevance": 0,
            "groundedness": 0,
            "helpfulness": 0,
            "reason": "Invalid judge output"
        }


def get_latest_customer_message(conversation):
    messages = conversation.split("\n")
    customer_messages = [
        msg.replace("CUSTOMER:", "", 1).strip()
        for msg in messages
        if msg.startswith("CUSTOMER:")
    ]
    return customer_messages[-1] if customer_messages else ""


if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)

    results = []

    # Start with 5 examples to validate the judge
    for _, row in df.head(5).iterrows():
        message = get_latest_customer_message(row["conversation"])
        response = generate_response(message)

        judgment = judge_response(message, response)

        results.append({
            "conversation_id": row["conversation_id"],
            "customer_message": message,
            "generated_response": response,
            **judgment
        })

        print("\nCustomer:", message)
        print("Response:", response)
        print("Judge:", judgment)

    pd.DataFrame(results).to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")