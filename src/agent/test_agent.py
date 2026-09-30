from .agent import run_agent


messages = [
    "Where is my package? It was supposed to arrive yesterday.",
    "Someone hacked my Amazon account.",
    "Thanks, that solved my problem.",
]

for message in messages:
    print("\n" + "=" * 60)
    print("CUSTOMER:", message)

    result = run_agent(message)

    print("INTENT:", result["intent"])
    print("RESPONSE:", result["response"])
    print("ESCALATE:", result["should_escalate"])
    print("REASON:", result["reason"])