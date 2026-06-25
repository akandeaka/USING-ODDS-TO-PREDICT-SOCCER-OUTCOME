import streamlit as st
import pandas as pd
import os

st.title("Full Performance Log")

if not os.path.exists("performance_log.csv"):
    st.info("No data yet.")
else:
    df = pd.read_csv("performance_log.csv")
    st.dataframe(df)
    st.download_button("Download Log", df.to_csv(index=False), "performance_log.csv")
