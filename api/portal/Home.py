import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Soccer Prediction Portal", layout="wide")

st.title("Soccer Outcome Prediction Engine")

st.markdown("""
Welcome to the prediction portal.  
This system fetches odds from BetMines, Forebet, and Soccerway, applies blueprint rules, 
and logs predictions with confidence.  
Use the sidebar to explore Dashboard, Predictions, Performance Log, and ML Insights.
""")

# Show today's predictions right on Home
st.subheader("Today's Predictions Snapshot")

if not os.path.exists("performance_log.csv"):
    st.info("No predictions yet. Scheduler will populate data.")
else:
    df = pd.read_csv("performance_log.csv")
    today = str(date.today())
    today_df = df[df["date"] == today]

    if today_df.empty:
        st.info("No predictions logged for today yet.")
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
                st.progress(conf)  # confidence bar
                st.caption(f"Confidence: {conf:.2f} | Status: {status}")

