import streamlit as st
import pandas as pd
import os
from datetime import date

st.title("Soccer Outcome Prediction Engine")

st.subheader("Today's Predictions Snapshot")

if not os.path.exists("performance_log.csv"):
    st.info("No predictions yet. Scheduler will populate data.")
else:
    df = pd.read_csv("performance_log.csv")
    today = str(date.today())
    today_df = df[df["date"] == today]

    if today_df.empty:
        st.error("⚠️ All scrapers failed today (Forebet, BetMines, Soccerway). Paste odds into manual_data/manual_matches.csv and rerun scheduler.")
    else:
        grouped = today_df.groupby("match_id")
        for match_id, group in grouped:
            league = group["league"].iloc[0]
            st.markdown(f"### {league} | {match_id}")
            for _, row in group.iterrows():
                signal = row["signals"]
                conf = row["ml_confidence"]
                status = row["status"]
                st.write(f"**Signal:** {signal}")
                st.progress(conf)
                st.caption(f"Confidence: {conf:.2f} | Status: {status}")
