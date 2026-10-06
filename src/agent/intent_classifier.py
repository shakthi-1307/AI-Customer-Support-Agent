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

        if any(x in text for x in [
            "contacted support",
            "contacted customer service",
            "nobody has solved",
            "no one has solved",
            "still not resolved",
            "third time",
            "multiple times",
            "supervisor",
            "manager"
        ]):
            return "Customer Service / Complaint"

        return self.model.predict([message])[0]