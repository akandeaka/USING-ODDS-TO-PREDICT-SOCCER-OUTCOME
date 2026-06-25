import streamlit as st
import pandas as pd
import os

st.title("ML Insights")

if not os.path.exists("performance_log.csv"):
    st.info("No data yet.")
else:
    df = pd.read_csv("performance_log.csv")
    if "ml_confidence" in df.columns:
        st.subheader("Confidence Distribution")
        st.bar_chart(df["ml_confidence"])

        st.subheader("Signals with Confidence")
        st.dataframe(df[["match_id", "league", "signals", "ml_confidence", "status"]])
    else:
        st.info("Train ML model and log confidence to see insights.")
