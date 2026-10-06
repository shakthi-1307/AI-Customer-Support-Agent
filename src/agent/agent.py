from src.rag.generate_response import generate_response
from .message_filter import is_acknowledgement
from .escalation import decide_escalation
from .intent_classifier import IntentClassifier


classifier = IntentClassifier()


def run_agent(customer_message):
    # 1. Ignore simple acknowledgements
    if is_acknowledgement(customer_message):
        return {
            "intent": "Other",
            "response": "",
            "should_escalate": False,
            "reason": "Customer acknowledgement; no response needed."
        }

    # 2. Classify intent
    intent = classifier.predict(customer_message)

    # 3. Check escalation
    escalation = decide_escalation(customer_message)

    # 4. Escalate instead of generating a response
    if escalation["should_escalate"]:
        return {
            "intent": intent,
            "response": "",
            "should_escalate": True,
            "reason": escalation["reason"]
        }

    # 5. Only non-escalated cases go through RAG + LLM
    response = generate_response(customer_message)

    return {
        "intent": intent,
        "response": response,
        "should_escalate": False,
        "reason": escalation["reason"]
    }