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
        # Overall accuracy
        overall = (df["status"] == "Correct").mean() * 100
        st.metric("Overall Accuracy", f"{overall:.1f}%")

        # Confidence-weighted accuracy (overall)
        if "ml_confidence" in df.columns:
            weighted_acc = (
                (df["ml_confidence"] * (df["status"] == "Correct").astype(int)).sum()
                / df["ml_confidence"].sum()
            ) * 100
            st.metric("Confidence-Weighted Accuracy", f"{weighted_acc:.1f}%")

        # Accuracy by Blueprint Signal (raw)
        st.subheader("Raw Accuracy by Blueprint Signal")
        df["signals"] = df["signals"].astype(str)
        acc_signal = (
            df.groupby("signals")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_values(ascending=False)
        )
        st.bar_chart(acc_signal)

        # Confidence-weighted accuracy by Blueprint Signal
        if "ml_confidence" in df.columns:
            st.subheader("Confidence-Weighted Accuracy by Blueprint Signal")
            weighted_acc_signal = (
                df.groupby("signals")
                .apply(lambda g: (g["ml_confidence"] * (g["status"] == "Correct").astype(int)).sum()
                       / g["ml_confidence"].sum() * 100)
                .sort_values(ascending=False)
            )
            st.bar_chart(weighted_acc_signal)

            # Table view
            perf_table = pd.DataFrame({
                "Blueprint": weighted_acc_signal.index,
                "Weighted Accuracy (%)": weighted_acc_signal.values
            })
            st.dataframe(perf_table)

        # Accuracy by League
        st.subheader("Accuracy by League")
        acc_league = (
            df.groupby("league")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_values(ascending=False)
        )
        st.bar_chart(acc_league)

        # Daily Hit Rate
        st.subheader("Daily Hit Rate")
        daily = (
            df.groupby("date")["status"]
            .apply(lambda x: (x == "Correct").mean() * 100)
            .sort_index()
        )
        st.line_chart(daily)
