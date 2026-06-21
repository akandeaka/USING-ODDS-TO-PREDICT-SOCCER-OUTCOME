import streamlit as st
import pandas as pd
import os

st.title("Full Performance Log")

if not os.path.exists("performance_log.csv"):
    st.info("No data yet.")
else:
    df = pd.read_csv("performance_log.csv")
    st.dataframe(df)
