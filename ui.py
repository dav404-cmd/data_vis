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

col1,col2 = st.columns(2)

with col1:
    # Plot salary distribution
    st.subheader("Salary Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['salary_filled'].dropna(), bins=20)
    ax.set_xlabel("Salary")
    ax.set_ylabel("Num of jobs")
    st.pyplot(fig)

with col2:
    st.subheader("Salary Spread (Boxplot)")

    fig2, ax2 = plt.subplots()
    ax2.boxplot(filtered_df['salary_filled'].dropna(), vert=False)
    ax2.set_xlabel("Salary")
    st.pyplot(fig2)

# Show top 10 jobs
st.subheader("Top 10 Highest Paying Jobs")
top10 = filtered_df.sort_values(by="salary_filled", ascending=False).head(10)
st.dataframe(top10[['title', 'company', 'salary_filled']])