import requests
from config import ADZUNA_APP_ID, ADZUNA_API_KEY

# Skills we want to detect in job descriptions
SKILLS_TO_TRACK = [
    "python", "sql", "spark", "kafka", "airflow", "dbt",
    "snowflake", "databricks", "aws", "gcp", "azure",
    "docker", "kubernetes", "terraform", "pandas", "pyspark",
    "redshift", "bigquery", "looker", "tableau", "powerbi",
    "langchain", "llm", "ai", "machine learning", "mlflow"
]

def fetch_jobs(job_title, num_results=20):
    print(f"Fetching live jobs for: {job_title}...\n")

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": num_results,
        "what": job_title,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data["results"]

def extract_skills(jobs):
    skill_count = {}

    for job in jobs:
        description = job["description"].lower()
        for skill in SKILLS_TO_TRACK:
            if skill in description:
                skill_count[skill] = skill_count.get(skill, 0) + 1

    return skill_count

def show_insights(job_title, jobs, skill_count):
    print(f"=== Market Insights for: {job_title} ===")
    print(f"Jobs analyzed: {len(jobs)}")
    print()

    # Sort skills by frequency
    sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)

    print("🔥 Most In-Demand Skills:")
    for skill, count in sorted_skills[:10]:
        bar = "█" * count
        print(f"  {skill:<20} {bar} ({count} jobs)")

    print()

    # Skills you already have
    your_skills = ["sql", "python", "dbt", "airflow", "snowflake", "tableau", "gcp"]
    missing = [s for s, c in sorted_skills[:15] if s not in your_skills]

    print("✅ Your skills that are in demand:")
    for skill, count in sorted_skills:
        if skill in your_skills:
            print(f"  ✓ {skill} — appears in {count} jobs")

    print()
    print("🚀 Top skills to learn next (gaps):")
    for skill in missing[:5]:
        count = skill_count.get(skill, 0)
        print(f"  → {skill} — appears in {count} jobs")

# Run it
jobs = fetch_jobs("data engineer", num_results=20)
skill_count = extract_skills(jobs)
show_insights("Data Engineer", jobs, skill_count)

if __name__ == "__main__":
    fetch_jobs("data engineer")
    skill_count = extract_skills(jobs)
    show_insights("Data Engineer", jobs, skill_count)