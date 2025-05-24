import json
from collections import Counter
import pandas as pd

def load_data(filepath="linkedin_jobs.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def analyze_jobs(data):
    df = pd.DataFrame(data)
    
    # Drop rows without title or location
    df = df.dropna(subset=["title", "location"])

    print("\n--- Top 5 Job Titles ---")
    top_titles = df["title"].value_counts().head(5)
    print(top_titles.to_string())

    print("\n--- Top 5 Companies ---")
    top_companies = df["company"].value_counts().head(5)
    print(top_companies.to_string())

    print("\n--- Top 5 Cities by Job Openings ---")
    top_cities = df["location"].value_counts().head(5)
    print(top_cities.to_string())

    print("\n--- Most Frequent Skills (from job titles, naive) ---")
    skills = []
    for title in df["title"]:
        words = title.lower().replace(",", " ").split()
        skills.extend(words)

    skills_counter = Counter(skills)
    ignore_words = {"and", "with", "for", "in", "the", "of", "a", "to", "on", "at"}
    filtered_skills = {k:v for k,v in skills_counter.items() if k not in ignore_words and len(k) > 2}
    top_skills = Counter(filtered_skills).most_common(10)

    for skill, count in top_skills:
        print(f"{skill}: {count}")

if __name__ == "__main__":
    jobs_data = load_data()
    analyze_jobs(jobs_data)
