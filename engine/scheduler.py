import time
from datetime import datetime
import schedule
import pandas as pd
from engine.data_sources import get_match_data
from blueprint_classifier import classify_match
from engine.performance import log_prediction, update_results, init_log
from engine.notifications import send_telegram


def morning_predictions() -> None:
    print("Running morning_predictions...")
    init_log()
    matches = get_match_data()
    lines = []

    for m in matches:
        signals = classify_match(m)  # returns list of dicts: {"signal":..., "strength":...}
        if not signals:
            continue

        for sig in signals:
            # baseline ML confidence = strength (later replaced by ML model)
            ml_conf = sig["strength"]
            log_prediction(m, [sig["signal"]], ml_conf)
            lines.append(
                f"{m['League']} | {m['MatchID']} → {sig['signal']} (strength={ml_conf:.2f})"
            )

    if lines:
        send_telegram("Today's predictions:\n" + "\n".join(lines))
    else:
        send_telegram("No predictions today.")


def night_results() -> None:
    print("Running night_results...")
    try:
        df = pd.read_csv("performance_log.csv")
    except FileNotFoundError:
        return

    # demo: mark all pending as Correct
    results = {row["match_id"]: True for _, row in df.iterrows() if row["status"] == "PENDING"}
    update_results(results)
    send_telegram("Night results updated.")


def main() -> None:
    print("Scheduler started at", datetime.now())
    init_log()

    schedule.every().day.at("09:00").do(morning_predictions)
    schedule.every().day.at("23:00").do(night_results)

    # run once immediately for testing
    morning_predictions()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
