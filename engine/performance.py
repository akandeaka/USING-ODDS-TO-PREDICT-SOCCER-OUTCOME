import csv
import os
from datetime import date
import pandas as pd

LOG_FILE = "performance_log.csv"


def init_log() -> None:
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["match_id", "league", "signals", "ml_confidence", "date", "status"]
            )


def log_prediction(match: dict, signals: list[str], ml_confidence: float) -> None:
    init_log()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                match["MatchID"],
                match["League"],
                "|".join(signals),
                ml_confidence,
                match.get("Date", str(date.today())),
                "PENDING",
            ]
        )


def update_results(results: dict[str, bool]) -> None:
    if not os.path.exists(LOG_FILE):
        return
    df = pd.read_csv(LOG_FILE)
    for idx, row in df.iterrows():
        mid = row["match_id"]
        if mid in results:
            df.at[idx, "status"] = "Correct" if results[mid] else "Wrong"
    df.to_csv(LOG_FILE, index=False)
