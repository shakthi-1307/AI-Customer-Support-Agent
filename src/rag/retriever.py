import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = "data/amazon_conversations_clean.csv"


class ConversationRetriever:

    def __init__(self, top_k=5):
        self.top_k = top_k

        self.df = pd.read_csv(DATA_PATH)

        self.df["conversation"] = (
            self.df["conversation"]
            .fillna("")
            .astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=30000,
        )

        self.embeddings = self.vectorizer.fit_transform(
            self.df["conversation"]
        )

    def retrieve(self, query):
        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.embeddings
        )[0]

        top_indices = scores.argsort()[-self.top_k:][::-1]

        results = []

        for index in top_indices:
            results.append({
                "conversation_id": int(
                    self.df.iloc[index]["conversation_id"]
                ),
                "score": float(scores[index]),
                "conversation": self.df.iloc[index]["conversation"],
            })

        return results