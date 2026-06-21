import streamlit as st
import pandas as pd
import os

st.title("Performance Dashboard")

if not os.path.exists("performance_log.csv"):
    st.info("No data yet. Run scheduler or create predictions first.")
else:
    df = pd.read_csv("performance_log.csv")
    if df.empty:
        st.info("Log is empty.")
    else:
        overall = (df["status"] == "Correct").mean() * 100
        st.metric("Overall Accuracy", f"{overall:.1f}%")

        df["signals"] = df["signals"].astype(str)
        st.subheader("Accuracy by Blueprint")
        acc_signal = (
            df.groupby("signals")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_values(ascending=False)
        )
        st.bar_chart(acc_signal)

        st.subheader("Accuracy by League")
        acc_league = (
            df.groupby("league")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_values(ascending=False)
        )
        st.bar_chart(acc_league)

        st.subheader("Daily Hit Rate")
        daily = (
            df.groupby("date")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_index()
        )
        st.line_chart(daily)
