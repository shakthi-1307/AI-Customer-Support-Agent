from .intent_classifier import IntentClassifier


classifier = IntentClassifier()

messages = [
    "Where is my package? It was supposed to arrive yesterday.",
    "I want to return this item.",
    "I was charged twice for my order.",
    "Someone hacked my account.",
    "My Kindle is not working.",
]

for message in messages:
    intent = classifier.predict(message)

    print("\nCustomer:", message)
    print("Intent:", intent)