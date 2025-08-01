import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

script_dir = Path(__file__).resolve().parent

file_path = script_dir/'data'/'data_cleaned'/"processed_data.csv"

df = pd.read_csv(file_path)

st.title("💼 Salary Dashboard")

location = st.selectbox("Select Location", df['location'].unique())
filtered_df = df[df['location'] == location]

st.write("Average Salary in", location, ":", filtered_df['salary_filled'].mean())

# Plot salary distribution
st.subheader("Salary Distribution")
fig, ax = plt.subplots()
ax.hist(filtered_df['salary_filled'].dropna(), bins=20)
st.pyplot(fig)

# Show top 10 jobs
st.subheader("Top 10 Highest Paying Jobs")
top10 = filtered_df.sort_values(by="salary_filled", ascending=False).head(10)
st.dataframe(top10[['title', 'company', 'salary_filled']])
