import streamlit as st
import json
import pandas as pd
from collections import Counter
import plotly.express as px

@st.cache_data
def load_data():
    with open("linkedin_jobs.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def preprocess_skills(jobs):
    skills_list = []
    for job in jobs:
        if job["skills"]:
            skills_list.extend(job["skills"])
        else:
            if job["title"]:
                skills_list.extend(job["title"].lower().split())
    return skills_list

def main():
    st.title("LinkedIn Job Trend Analyzer")

    data = load_data()
    df = pd.DataFrame(data)

    keyword = st.text_input("Filter by keyword (e.g. Data Analyst):", value="")

    if keyword:
        df = df[df["title"].str.contains(keyword, case=False, na=False)]

    st.subheader("Top 5 Most In-Demand Job Titles")
    top_titles = df["title"].value_counts().head(5)
    st.bar_chart(top_titles)

    st.subheader("Top 5 Companies")
    top_companies = df["company"].value_counts().head(5)
    st.bar_chart(top_companies)

    st.subheader("Cities with Highest Number of Openings")
    top_cities = df["location"].value_counts().head(5)
    st.bar_chart(top_cities)

    st.subheader("Most Frequent Skills (naive from titles)")
    skills = preprocess_skills(df.to_dict(orient="records"))
    skills_counter = Counter(skills)
    common_skills = pd.DataFrame(skills_counter.most_common(10), columns=["Skill", "Count"])
    st.bar_chart(common_skills.set_index("Skill"))

if __name__ == "__main__":
    main()
