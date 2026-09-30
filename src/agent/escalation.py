ESCALATION_KEYWORDS = [
    "fraud",
    "scam",
    "hacked",
    "unauthorized",
    "charged twice",
    "charged me",
    "account compromised",
    "legal",
    "lawsuit",
    "police",
]


def decide_escalation(customer_message):
    text = customer_message.lower()

    for keyword in ESCALATION_KEYWORDS:
        if keyword in text:
            return {
                "should_escalate": True,
                "reason": f"Potential high-risk issue: {keyword}"
            }

    return {
        "should_escalate": False,
        "reason": "No high-risk escalation indicator detected."
    }