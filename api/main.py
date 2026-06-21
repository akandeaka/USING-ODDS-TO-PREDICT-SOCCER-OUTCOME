from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from datetime import date

app = FastAPI()


class Prediction(BaseModel):
    match_id: str
    league: str
    signals: str
    ml_confidence: float
    status: str = "PENDING"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predictions/today")
def get_today_predictions():
    if not os.path.exists("performance_log.csv"):
        return []
    df = pd.read_csv("performance_log.csv")
    today = str(date.today())
    return df[df["date"] == today].to_dict(orient="records")


@app.post("/predictions")
def create_prediction(p: Prediction):
    if os.path.exists("performance_log.csv"):
        df = pd.read_csv("performance_log.csv")
    else:
        df = pd.DataFrame(
            columns=["match_id", "league", "signals", "ml_confidence", "date", "status"]
        )
    new_row = {
        "match_id": p.match_id,
        "league": p.league,
        "signals": p.signals,
        "ml_confidence": p.ml_confidence,
        "date": str(date.today()),
        "status": p.status,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("performance_log.csv", index=False)
    return {"status": "created"}
