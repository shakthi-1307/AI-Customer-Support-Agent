import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATA_PATH = "data/golden_set.csv"


class IntentClassifier:

    def __init__(self):
        df = pd.read_csv("data/golden_set.csv")

        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=30000,
                sublinear_tf=True
            )),
            ("classifier", LogisticRegression(
                max_iter=2000,
                class_weight="balanced"
            ))
        ])

        self.model.fit(
            df["conversation"],
            df["intent"]
        )

    def predict(self, message):
        text = message.lower()

        if "refund" in text:
            return "Refund"

        if any(x in text for x in [
            "fraud", "scam", "hacked", "unauthorized", "stolen"
        ]):
            return "Security / Fraud"

        if any(x in text for x in [
            "contacted support", "customer service",
            "nobody has solved", "no one has solved",
            "still not resolved", "supervisor", "manager"
        ]):
            return "Customer Service / Complaint"

        if any(x in text for x in [
            "where is my package", "where is my order",
            "tracking", "package hasn't arrived",
            "package has not arrived"
        ]):
            return "Delivery / Tracking"
        
        if any(x in text for x in [
            "charged twice", "charged me", "double charged",
            "billing", "payment"
        ]):
            return "Payment / Billing"

        if any(x in text for x in [
            "can't login", "cannot login", "can't log in",
            "cannot log in", "forgot password", "account locked"
        ]):
            return "Account / Login"

        if any(x in text for x in [
            "prime membership", "cancel prime",
            "cancel my prime", "prime subscription"
        ]):
            return "Prime Membership"

        return self.model.predict([message])[0]