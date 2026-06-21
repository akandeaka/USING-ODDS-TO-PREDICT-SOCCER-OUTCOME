from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class Prediction(BaseModel):
    match_id: str
    league: str
    signals: str
    ml_confidence: float
    priority: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predictions/today")
def get_today_predictions():
    df = pd.read_csv("performance_log.csv")
    today = str(pd.Timestamp.today().date())
    return df[df["date"] == today].to_dict(orient="records")

@app.post("/predictions")
def create_prediction(p: Prediction):
    df = pd.read_csv("performance_log.csv")
    new_row = {
        "match_id": p.match_id,
        "league": p.league,
        "signals": p.signals,
        "ml_confidence": p.ml_confidence,
        "date": str(pd.Timestamp.today().date()),
        "status": "PENDING"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("performance_log.csv", index=False)
    return {"status": "created"}
