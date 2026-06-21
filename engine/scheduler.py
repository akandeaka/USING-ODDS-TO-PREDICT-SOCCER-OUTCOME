import time
from datetime import datetime
import schedule
import pandas as pd
from engine.data_sources import get_match_data
from engine.blueprint_classifier import classify_match
from engine.performance import log_prediction, update_results
from engine.notifications import send_telegram


def morning_predictions() -> None:
    matches = get_match_data()
    if not matches:
        return
    lines = []
    for m in matches:
        signals = classify_match(m)
        if not signals:
            continue
        # placeholder ML confidence until model is integrated
        ml_conf = 0.8
        log_prediction(m, signals, ml_conf)
        lines.append(
            f"{m['League']} | {m['MatchID']} → {signals} (conf={ml_conf:.2f})"
        )
    if lines:
        send_telegram("Today's predictions:\n" + "\n".join(lines))


def night_results() -> None:
    # demo: randomly mark all pending as Correct
    try:
        df = pd.read_csv("performance_log.csv")
    except FileNotFoundError:
        return
    results = {row["match_id"]: True for _, row in df.iterrows() if row["status"] == "PENDING"}
    update_results(results)
    send_telegram("Night results updated.")


def main() -> None:
    print("Scheduler started at", datetime.now())
    schedule.every().day.at("09:00").do(morning_predictions)
    schedule.every().day.at("23:00").do(night_results)
    # for testing: run immediately once
    morning_predictions()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
    from engine.performance import init_log

def main():
    init_log()  # ensure CSV exists
    morning_predictions()
    night_results()
    # then enter schedule loop...

