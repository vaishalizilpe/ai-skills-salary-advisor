# 🤖 AI Skills & Salary Advisor

A live job market analyzer that fetches real job postings and uses 
Claude AI to give personalized career advice for data professionals.

## What It Does

1. Fetches live job postings from Adzuna API (real 2026 data)
2. Extracts in-demand skills from job descriptions automatically
3. Compares market demand against your current skill set
4. Uses Claude AI to generate brutally honest, personalized career advice

## Demo Output
```
🔥 Most In-Demand Skills:
  ai                   ██████████ (10 jobs)
  snowflake            ███ (3 jobs)
  python               ██ (2 jobs)

✅ Your skills that are in demand:
  ✓ snowflake — appears in 3 jobs
  ✓ python — appears in 2 jobs

🚀 Top skills to learn next:
  → LLM Orchestration
  → Databricks
  → RAG Pipelines
```

## Tech Stack

Python · Adzuna Jobs API · Anthropic Claude API · pandas

## Setup

1. Clone the repo
2. Install dependencies
```bash
   pip install requests anthropic
```
3. Set your API keys as environment variables
```bash
   export ANTHROPIC_API_KEY="your_key"
   export ADZUNA_APP_ID="your_app_id"
   export ADZUNA_API_KEY="your_api_key"
```
4. Run it
```bash
   python ai_advisor.py
```

## Why I Built This

I'm a data engineer with 11 years of experience transitioning into 
AI engineering. I built this tool because I needed it myself — a way 
to see what the market actually wants right now, not 2 years ago.

## Part of My AI Engineering Journey

This is Project 2 of my 6-project AI portfolio. Each project builds 
on the last, combining my data engineering background with modern 
AI tooling.

👉 [See all projects](https://github.com/vaishalizilpe)