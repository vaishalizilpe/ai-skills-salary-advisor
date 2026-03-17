# AI Career Intelligence — Skills & Salary Advisor

**[→ Try it live: ai-skills-career-advisor.streamlit.app](https://ai-skills-career-advisor.streamlit.app)**

---

Most career advice is based on vibes. This tool is based on data.

It pulls real job postings from today's market, uses Claude AI to read every description and extract every skill mentioned, compares that against what you know, and tells you exactly where you stand — and what to do next.

No guessing. No generic advice. Just the market, reflected back at you.

---

## What It Does

You pick a role, a location, a salary range, and your current skills. Then:

1. **20+ live job postings are fetched** from the Adzuna Jobs API — real listings, posted today
2. **Claude AI reads every description** and extracts every skill, tool, and technology mentioned across all of them
3. **You see the market ranked** — which skills appear in the most jobs, and what percentage of listings require them
4. **Your gaps are surfaced** — what the market wants that you don't yet have
5. **Average salary is shown** — pulled from actual postings for that role and location, not survey estimates
6. **Claude gives you a personalized assessment** — direct, specific, no fluff
7. **Download the full report** as a `.txt` file to keep or share

---

## Why I Built This

I'm a data engineer with 11 years of experience. In 2026, I started transitioning into AI engineering and quickly realized: I had no idea what the market actually wanted right now.

Job boards were noise. Skill lists were generic. Everyone had an opinion, nobody had data.

So I built this. I needed something that would tell me — today, for this role, in this city, at this salary — what skills are showing up in real postings, what I'm missing, and what to learn next.

It's been more useful than any career coach I've talked to.

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Job data | Adzuna Jobs API |
| Skill extraction | Anthropic Claude (`claude-opus-4-5`) |
| Career advice | Anthropic Claude (`claude-opus-4-5`) |
| Language | Python |

---

## Run It Yourself

**1. Clone**
```bash
git clone https://github.com/vaishalizilpe/ai-skills-salary-advisor.git
cd ai-skills-salary-advisor
```

**2. Install**
```bash
pip install requests anthropic streamlit
```

**3. Add API keys**

Local:
```bash
export ANTHROPIC_API_KEY="your_key"
export ADZUNA_APP_ID="your_app_id"
export ADZUNA_API_KEY="your_api_key"
```

Streamlit Cloud (`Settings → Secrets`):
```toml
ANTHROPIC_API_KEY = "your_key"
ADZUNA_APP_ID = "your_app_id"
ADZUNA_API_KEY = "your_api_key"
```

**4. Run**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

**Get your API keys:**
- Anthropic: [console.anthropic.com](https://console.anthropic.com)
- Adzuna: [developer.adzuna.com](https://developer.adzuna.com)

---

## Project Structure

```
app.py            # Streamlit UI — inputs, results, download
job_fetcher.py    # Adzuna API + Claude skill extraction
ai_advisor.py     # Claude career advice generation
config.py         # Configuration
```

---

## Part of My AI Engineering Portfolio

This is Project 2 of 6. Each project builds on the last — combining 11 years of data engineering experience with modern AI tooling.

[See all projects → github.com/vaishalizilpe](https://github.com/vaishalizilpe)
