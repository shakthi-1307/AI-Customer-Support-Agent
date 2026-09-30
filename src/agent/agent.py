from src.rag.generate_response import generate_response
from .message_filter import is_acknowledgement
from .escalation import decide_escalation
from .intent_classifier import IntentClassifier


classifier = IntentClassifier()


def run_agent(customer_message):

    if is_acknowledgement(customer_message):
        return {
            "intent": "Other",
            "response": "",
            "should_escalate": False,
            "reason": "Customer acknowledgement; no response needed."
        }

    intent = classifier.predict(customer_message)

    escalation = decide_escalation(customer_message)

    response = generate_response(customer_message)

    return {
        "intent": intent,
        "response": response,
        "should_escalate": escalation["should_escalate"],
        "reason": escalation["reason"]
    }