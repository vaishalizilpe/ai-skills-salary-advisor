import requests
import os
import anthropic
import json

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_API_KEY = os.environ.get("ADZUNA_API_KEY", "")


def fetch_jobs(job_title, num_results=20, salary_min=None, salary_max=None, location=None):
    print(f"Fetching live jobs for: {job_title}...")

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": num_results,
        "what": job_title,
        "content-type": "application/json"
    }
    if salary_min is not None:
        params["salary_min"] = salary_min
    if salary_max is not None:
        params["salary_max"] = salary_max
    if location:
        params["where"] = location

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Adzuna API error: status {response.status_code} | body: {response.text[:200]}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"JSON decode failed: {e} | raw: {response.text[:200]}")

    if "results" not in data:
        raise Exception(f"No results key in response: {str(data)[:200]}")

    return data["results"]


def extract_skills_with_ai(jobs):
    """Use Claude to dynamically extract skills from job descriptions."""

    all_descriptions = ""
    for i, job in enumerate(jobs):
        desc = job.get("description", "")[:500]
        all_descriptions += f"Job {i+1}: {desc}\n\n"

    prompt = f"""You are analyzing {len(jobs)} real job postings.

Here are the job descriptions:
{all_descriptions}

Extract ALL technical skills, tools, languages, platforms, and frameworks mentioned across these job postings.
Count how many job postings mention each skill.

Return ONLY a valid JSON object like this example:
{{"python": 14, "sql": 12, "spark": 8, "aws": 10, "dbt": 6}}

Rules:
- Lowercase all skill names
- Normalize variations: "apache spark" -> "spark", "power bi" -> "powerbi", "amazon web services" -> "aws"
- Only include technical skills, not soft skills
- Return ONLY the JSON object, no explanation, no markdown, no backticks
"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise Exception(f"Claude returned invalid JSON: {raw[:200]}")


if __name__ == "__main__":
    jobs = fetch_jobs("data engineer", num_results=20)
    skill_count = extract_skills_with_ai(jobs)
    sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
    print("Top skills:")
    for skill, count in sorted_skills[:15]:
        print(f"  {skill}: {count}")