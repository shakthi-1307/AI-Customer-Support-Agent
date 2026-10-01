ESCALATION_KEYWORDS = [
    "fraud",
    "scam",
    "hacked",
    "unauthorized",
    "account compromised",
    "charged twice",
    "charged me",
    "refund not received",
    "not been refunded",
    "first payment",
    "legal",
    "lawsuit",
    "police",
]

UNRESOLVED_KEYWORDS = [
    "third time",
    "third one",
    "multiple times",
    "twice already",
    "again",
    "still not resolved",
    "no further help",
    "no help",
    "no solution",
    "supervisor",
    "manager",
    "contacted support",
    "spoken to",
    "generic response",
    "broken promises",
]


def decide_escalation(customer_message):
    text = customer_message.lower()

    for keyword in ESCALATION_KEYWORDS:
        if keyword in text:
            return {
                "should_escalate": True,
                "reason": f"Potential high-risk issue: {keyword}"
            }

    for keyword in UNRESOLVED_KEYWORDS:
        if keyword in text:
            return {
                "should_escalate": True,
                "reason": f"Potential unresolved issue: {keyword}"
            }

    return {
        "should_escalate": False,
        "reason": "No escalation indicator detected."
    }