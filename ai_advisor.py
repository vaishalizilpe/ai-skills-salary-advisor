import anthropic
import os
from job_fetcher import fetch_jobs, extract_skills

os.environ["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY", "")

def get_ai_advice(job_title, skill_count, your_skills):
    # Build context from real job data
    sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
    market_skills = [f"{skill} ({count} jobs)" for skill, count in sorted_skills[:15]]
    missing = [s for s, _ in sorted_skills[:15] if s not in your_skills]

    prompt = f"""
You are a sharp, direct career advisor for data professionals.

Here is LIVE job market data for '{job_title}' roles (scraped today):

Most in-demand skills right now:
{chr(10).join(market_skills)}

This professional's current skills:
{', '.join(your_skills)}

Their skill gaps based on market data:
{', '.join(missing[:8])}

Give them:
1. A brutally honest assessment of where they stand
2. The top 3 skills to learn next and exactly why
3. A realistic timeline to become more competitive
4. One sentence on what makes them already valuable

Be direct, specific, and encouraging. No fluff.
"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

# Run it
print("Fetching live market data...")
jobs = fetch_jobs("data engineer", num_results=20)
skill_count = extract_skills(jobs)

your_skills = ["sql", "python", "dbt", "airflow", "snowflake", "tableau", "gcp"]

print("\n🤖 AI Career Advisor says:\n")
print("=" * 60)
advice = get_ai_advice("Data Engineer", skill_count, your_skills)
print(advice)
print("=" * 60)

if __name__ == "__main__":
    print("Fetching live market data...")
    jobs = fetch_jobs("data engineer", num_results=20)
    skill_count = extract_skills(jobs)

    your_skills = ["sql", "python", "dbt", "airflow", "snowflake", "tableau", "gcp"]

    print("\n🤖 AI Career Advisor says:\n")
    print("=" * 60)
    advice = get_ai_advice("Data Engineer", skill_count, your_skills)
    print(advice)
    print("=" * 60)