import pandas as pd
import streamlit as st

# Load the data
df = pd.read_csv("./cache/nfl_team_stats.csv")
st.write(df)