import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


DATA_PATH = "data/baseline_data.csv"

df = pd.read_csv(DATA_PATH)

df["conversation"] = df["conversation"].fillna("").astype(str)
df["intent"] = df["intent"].fillna("").astype(str)

df = df[df["conversation"].str.strip() != ""]
df = df[df["intent"].str.strip() != ""]

X = df["conversation"]
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000,
        ),
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        ),
    ),
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
macro_f1 = f1_score(
    y_test,
    predictions,
    average="macro",
    zero_division=0,
)

print("\n=== BASELINE 2 EVALUATION ===")
print(f"Accuracy : {accuracy:.4f}")
print(f"Macro-F1 : {macro_f1:.4f}")

print("\n=== CLASSIFICATION REPORT ===")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0,
    )
)

print("\n=== CONFUSION MATRIX ===")

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    predictions,
    labels=labels,
)

print(pd.DataFrame(
    cm,
    index=labels,
    columns=labels,
))