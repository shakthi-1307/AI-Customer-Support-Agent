import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


DATA_PATH = "data/golden_set.csv"


class IntentClassifier:

    def __init__(self):
        df = pd.read_csv(DATA_PATH)

        df["conversation"] = df["conversation"].fillna("")
        df["intent"] = df["intent"].fillna("")

        df = df[df["intent"].str.strip() != ""]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )

        X = self.vectorizer.fit_transform(df["conversation"])

        self.model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )

        self.model.fit(X, df["intent"])

    def predict(self, message):
        X = self.vectorizer.transform([message])
        return self.model.predict(X)[0]