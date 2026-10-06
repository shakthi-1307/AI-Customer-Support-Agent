from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

JUDGE_FILE = Path("data/response_judge_results.csv")
HUMAN_FILE = Path("data/human_ratings.csv")

RATING_COLUMNS = [
    "human_relevance",
    "human_groundedness",
    "human_helpfulness",
    "human_reason",
]


def load_data():
    if not JUDGE_FILE.exists():
        raise HTTPException(404, "Judge results file not found")

    judge = pd.read_csv(JUDGE_FILE)

    if HUMAN_FILE.exists():
        human = pd.read_csv(HUMAN_FILE)
    else:
        human = judge[["customer_message", "generated_response"]].copy()
        for col in RATING_COLUMNS:
            human[col] = ""

    if len(human) != len(judge):
        raise HTTPException(500, "Human ratings and judge files do not align")

    return judge, human


class Rating(BaseModel):
    relevance: int
    groundedness: int
    helpfulness: int
    reason: str = ""


@app.get("/api/items")
def get_items():
    judge, human = load_data()

    items = []

    for i, row in judge.iterrows():
        saved = human.iloc[i]

        def clean(value):
            if pd.isna(value):
                return ""
            return str(value)

        items.append({
            "id": i,
            "customer_message": clean(row["customer_message"]),
            "generated_response": clean(row["generated_response"]),
            "human_relevance": clean(saved["human_relevance"]),
            "human_groundedness": clean(saved["human_groundedness"]),
            "human_helpfulness": clean(saved["human_helpfulness"]),
            "human_reason": clean(saved["human_reason"]),
        })

    return items

@app.put("/api/ratings/{item_id}")
def save_rating(item_id: int, rating: Rating):
    if any(score < 1 or score > 5 for score in [
        rating.relevance,
        rating.groundedness,
        rating.helpfulness,
    ]):
        raise HTTPException(400, "Ratings must be between 1 and 5")

    judge, human = load_data()

    if item_id < 0 or item_id >= len(human):
        raise HTTPException(404, "Example not found")

    human.loc[item_id, "human_relevance"] = rating.relevance
    human.loc[item_id, "human_groundedness"] = rating.groundedness
    human.loc[item_id, "human_helpfulness"] = rating.helpfulness
    human.loc[item_id, "human_reason"] = rating.reason

    human.to_csv(HUMAN_FILE, index=False)
    return {"message": "Rating saved"}