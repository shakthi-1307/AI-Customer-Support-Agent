import pandas as pd
from sklearn.metrics import cohen_kappa_score

llm_df = pd.read_csv("data/response_judge_results.csv")
human_df = pd.read_csv("data/human_ratings.csv")

metrics = ["relevance", "groundedness", "helpfulness"]

if len(llm_df) != len(human_df):
    raise ValueError("The files have different numbers of rows.")

for metric in metrics:
    llm_scores = pd.to_numeric(llm_df[metric], errors="coerce")
    human_scores = pd.to_numeric(
        human_df[f"human_{metric}"], errors="coerce"
    )

    valid = llm_scores.notna() & human_scores.notna()
    llm = llm_scores[valid]
    human = human_scores[valid]

    if len(llm) == 0:
        print(f"\n{metric}: No valid ratings")
        continue

    agreement = (llm == human).mean()
    mae = (llm - human).abs().mean()
    kappa = cohen_kappa_score(
        human, llm, weights="quadratic"
    )

    print(f"\n{metric.capitalize()}")
    print(f"Valid pairs: {len(llm)}")
    print(f"Exact agreement: {agreement:.2f}")
    print(f"Mean absolute difference: {mae:.2f}")
    print(f"Weighted Cohen's kappa: {kappa:.2f}")