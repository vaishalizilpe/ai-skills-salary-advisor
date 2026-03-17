# AI Career Intelligence — Skills & Salary Advisor

**[🚀 Live Demo → ai-skills-career-advisor.streamlit.app](https://ai-skills-career-advisor.streamlit.app)**

A live job market analyzer that fetches real job postings, uses Claude AI to extract in-demand skills, and gives personalized career advice for data professionals.

## Features

- **Live job search** — pulls real postings from the Adzuna Jobs API
- **Salary range filter** — narrow results by target compensation ($40k–$300k)
- **AI skill extraction** — Claude reads every job description and dynamically extracts all mentioned skills
- **Skill gap analysis** — compares market demand against your current skill set
- **AI career assessment** — Claude generates a direct, personalized action plan
- **Download results** — export your full analysis as a `.txt` report

## How It Works

1. Select your target role and salary range
2. Choose your current skills from the multi-select list
3. Click **Analyze My Market Position**
4. Claude AI reads 20+ live job descriptions, counts every skill mentioned, and compares against yours
5. Get a brutally honest gap analysis and career advice — then download the report

## Tech Stack

Python · Streamlit · Adzuna Jobs API · Anthropic Claude API (`claude-opus-4-5`)

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/vaishalizilpe/ai-skills-salary-advisor.git
cd ai-skills-salary-advisor
```

**2. Install dependencies**
```bash
pip install requests anthropic streamlit
```

**3. Set API keys**

For local development, export as environment variables:
```bash
export ANTHROPIC_API_KEY="your_key"
export ADZUNA_APP_ID="your_app_id"
export ADZUNA_API_KEY="your_api_key"
```

For Streamlit Cloud, add them to your app's **Secrets** (`Settings → Secrets`):
```toml
ANTHROPIC_API_KEY = "your_key"
ADZUNA_APP_ID = "your_app_id"
ADZUNA_API_KEY = "your_api_key"
```

**4. Run**
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## API Keys

| Service | Where to get it |
|---|---|
| Anthropic Claude | [console.anthropic.com](https://console.anthropic.com) |
| Adzuna Jobs API | [developer.adzuna.com](https://developer.adzuna.com) |

## Project Structure

```
app.py            # Streamlit UI and app logic
job_fetcher.py    # Adzuna API calls + Claude skill extraction
ai_advisor.py     # Claude career advice generation
config.py         # Configuration
```

## Why I Built This

I'm a data engineer with 11 years of experience transitioning into AI engineering. I built this because I needed it myself — a way to see what the market actually wants right now, not 2 years ago.

## Part of My AI Engineering Journey

This is Project 2 of my 6-project AI portfolio. Each project builds on the last, combining my data engineering background with modern AI tooling.

[See all projects on GitHub](https://github.com/vaishalizilpe)
