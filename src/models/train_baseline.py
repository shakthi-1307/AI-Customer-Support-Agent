import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


DATA_PATH = "data/baseline_data.csv"

df = pd.read_csv(DATA_PATH)

df["input_text"] = df["input_text"].fillna("").astype(str)
df = df[df["input_text"].str.strip() != ""]

X = df["conversation"]
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\n=== BASELINE 1: TF-IDF + LOGISTIC REGRESSION ===")
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

print("\n=== CLASSIFICATION REPORT ===")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)