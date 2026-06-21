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
        st.dataframe(today_df)
