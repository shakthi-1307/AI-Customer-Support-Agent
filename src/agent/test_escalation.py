from .escalation import decide_escalation


messages = [
    "Someone hacked my Amazon account.",
    "I was charged twice for the same order.",
    "Where is my package?",
    "Thanks, that solved my problem.",
]

for message in messages:
    print("\nCustomer:", message)
    print(decide_escalation(message))