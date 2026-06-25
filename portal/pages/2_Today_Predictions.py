import streamlit as st
import pandas as pd
from datetime import date
import os

st.title("Today's Predictions")

if not os.path.exists("performance_log.csv"):
    st.info("No data yet.")
else:
    df = pd.read_csv("performance_log.csv")
    today = str(date.today())
    today_df = df[df["date"] == today]

    if today_df.empty:
        st.info("No predictions logged for today yet.")
    else:
        st.subheader("Match Predictions")

        # Group by match_id so multiple signals show together
        grouped = today_df.groupby("match_id")

        for match_id, group in grouped:
            league = group["league"].iloc[0]
            st.markdown(f"### {league} | {match_id}")

            for _, row in group.iterrows():
                signal = row["signals"]
                conf = row["ml_confidence"]
                status = row["status"]

                st.write(f"**Signal:** {signal}")
                st.progress(conf)  # confidence bar
                st.caption(f"Confidence: {conf:.2f} | Status: {status}")
