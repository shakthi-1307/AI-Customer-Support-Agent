import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from src.agent.escalation import decide_escalation


DATA_PATH = "data/golden_set.csv"
OUTPUT_PATH = "data/agent_evaluation_results.csv"


# Load data
df = pd.read_csv(DATA_PATH)
df["conversation"] = df["conversation"].fillna("").astype(str)
df["intent"] = df["intent"].fillna("").astype(str)
df["should_escalate"] = df["should_escalate"].astype(str).str.lower()

df = df[
    (df["conversation"].str.strip() != "")
    & (df["intent"].str.strip() != "")
    & (df["should_escalate"].isin(["true", "false"]))
].copy()

df["should_escalate"] = df["should_escalate"] == "true"

# Split data
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["intent"],
)

# Train intent classifier only on training data
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    max_features=10000,
)

X_train = vectorizer.fit_transform(train_df["conversation"])
X_test = vectorizer.transform(test_df["conversation"])

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
)

model.fit(X_train, train_df["intent"])

intent_predictions = model.predict(X_test)

# Intent evaluation
print("\n=== INTENT EVALUATION ===")
print("Accuracy:", accuracy_score(test_df["intent"], intent_predictions))
print("Macro-F1:", f1_score(
    test_df["intent"],
    intent_predictions,
    average="macro",
    zero_division=0,
))

print("\nClassification Report:")
print(classification_report(
    test_df["intent"],
    intent_predictions,
    zero_division=0,
))

print("Confusion Matrix:")
print(confusion_matrix(
    test_df["intent"],
    intent_predictions,
    labels=model.classes_,
))

# Escalation evaluation using the current rule-based baseline
escalation_predictions = test_df["conversation"].apply(
    lambda conversation: decide_escalation(conversation)["should_escalate"]
)

print("\n=== ESCALATION EVALUATION ===")
print(classification_report(
    test_df["should_escalate"],
    escalation_predictions,
    labels=[False, True],
    target_names=["Auto-handle", "Escalate"],
    zero_division=0,
))

print("Escalation Macro-F1:", f1_score(
    test_df["should_escalate"],
    escalation_predictions,
    average="macro",
    zero_division=0,
))

# Save predictions for error analysis
results = test_df[
    ["conversation_id", "conversation", "intent", "should_escalate"]
].copy()

results["predicted_intent"] = intent_predictions
results["predicted_escalation"] = escalation_predictions
results["intent_correct"] = (
    results["intent"] == results["predicted_intent"]
)
results["escalation_correct"] = (
    results["should_escalate"] == results["predicted_escalation"]
)

results.to_csv(OUTPUT_PATH, index=False)

print(f"\nResults saved to: {OUTPUT_PATH}")