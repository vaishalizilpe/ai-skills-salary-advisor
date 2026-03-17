import streamlit as st
import os

# Load secrets
try:
    os.environ["ADZUNA_APP_ID"] = st.secrets["ADZUNA_APP_ID"]
    os.environ["ADZUNA_API_KEY"] = st.secrets["ADZUNA_API_KEY"]
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
except KeyError as e:
    st.error(f"Missing secret: {e}. Check your Streamlit secrets configuration.")
    st.stop()

from job_fetcher import fetch_jobs, extract_skills_with_ai, fetch_salary_estimate
from ai_advisor import get_ai_advice

st.set_page_config(
    page_title="AI Career Intelligence | by Vaishali Zilpe",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 760px; }

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f2744 100%);
    border-radius: 16px; padding: 2.5rem 2rem; margin-bottom: 2rem;
    border: 1px solid #1e3a5f; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block; background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3); color: #60a5fa;
    padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1rem;
    font-family: 'DM Mono', monospace;
}
.hero h1 { color: #f8fafc; font-size: 2rem; font-weight: 700; margin: 0 0 0.75rem 0; line-height: 1.2; letter-spacing: -0.02em; }
.hero h1 span { color: #60a5fa; }
.hero p { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin: 0 0 1.5rem 0; }
.hero-stats { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; }
.hero-stat .number { color: #f8fafc; font-size: 1.1rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.hero-stat .label { color: #64748b; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; }

.how-it-works { background: #f8fafc; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0; }
.how-it-works h3 { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 1rem 0; color: #64748b; }
.steps { display: flex; gap: 1rem; flex-wrap: wrap; }
.step { display: flex; align-items: flex-start; gap: 0.6rem; flex: 1; min-width: 140px; }
.step-num { background: #0f172a; color: white; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; flex-shrink: 0; font-family: 'DM Mono', monospace; }
.step-text { color: #334155; font-size: 0.82rem; line-height: 1.4; }

.input-label { color: #0f172a; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.3rem; margin-top: 0.5rem; }
.input-hint { color: #94a3b8; font-size: 0.75rem; margin-bottom: 0.5rem; }

.results-header { background: #0f172a; color: #f8fafc; border-radius: 10px; padding: 1rem 1.25rem; margin: 1.5rem 0 1rem 0; font-size: 0.8rem; font-family: 'DM Mono', monospace; border-left: 3px solid #3b82f6; }
.section-title { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin: 1.5rem 0 0.75rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid #e2e8f0; }

.skill-bar-container { margin-bottom: 0.6rem; }
.skill-bar-label { display: flex; justify-content: space-between; margin-bottom: 4px; }
.skill-name { font-size: 0.82rem; font-weight: 500; color: #1e293b; font-family: 'DM Mono', monospace; }
.skill-count { font-size: 0.75rem; color: #94a3b8; font-family: 'DM Mono', monospace; }
.skill-bar-track { height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.skill-bar-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #60a5fa); border-radius: 3px; }

.tag-container { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.5rem 0; }
.tag-have { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 500; font-family: 'DM Mono', monospace; }
.tag-missing { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 500; font-family: 'DM Mono', monospace; }

.ai-advice-box { background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #3b82f6; border-radius: 0 10px 10px 0; padding: 1.5rem; margin-top: 1rem; font-size: 0.88rem; line-height: 1.7; color: #1e293b; }
.footer { text-align: center; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.75rem; }
.footer a { color: #3b82f6; text-decoration: none; }
.rate-badge { display: inline-block; background: #f1f5f9; border: 1px solid #e2e8f0; color: #64748b; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-family: 'DM Mono', monospace; margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Rate limiter
if "request_count" not in st.session_state:
    st.session_state.request_count = 0
MAX_REQUESTS = 3

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-tag">📊 Live Job Market Intelligence</div>
    <h1>AI <span>Career</span> Advisor</h1>
    <p>Enter your target role and current skills. This tool pulls real job postings from today's market,
    uses Claude AI to extract every skill mentioned, and gives you a brutally honest assessment
    of where you stand and exactly what to do next.</p>
    <div class="hero-stats">
        <div class="hero-stat"><span class="number">20+</span><span class="label">Live jobs analyzed</span></div>
        <div class="hero-stat"><span class="number">AI-powered</span><span class="label">Skill extraction</span></div>
        <div class="hero-stat"><span class="number">Claude AI</span><span class="label">Powering advice</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# HOW IT WORKS
st.markdown("""
<div class="how-it-works">
    <h3>How it works</h3>
    <div class="steps">
        <div class="step"><div class="step-num">1</div><div class="step-text">Fetches live job postings from Adzuna API</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-text">Claude AI reads every description and extracts skills dynamically</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-text">Compares market demand against your selected skills</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-text">Claude AI gives you personalized, direct career advice</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# INPUTS

JOB_TITLES = sorted([
    "Data Engineer", "Senior Data Engineer", "Staff Data Engineer",
    "Analytics Engineer", "Senior Analytics Engineer", "Staff Analytics Engineer",
    "Data Scientist", "Senior Data Scientist", "Machine Learning Engineer",
    "AI Engineer", "ML Platform Engineer", "Data Platform Engineer",
    "AI Product Analyst", "Business Intelligence Engineer", "BI Developer",
    "Data Analyst", "Senior Data Analyst", "Product Analyst",
    "Data Architect", "Cloud Data Engineer", "ETL Developer",
    "LLM Engineer", "AI/ML Data Engineer", "Generative AI Engineer"
])

st.markdown('<div class="input-label">Target Role</div>', unsafe_allow_html=True)
st.markdown('<div class="input-hint">Select the role you are applying for or transitioning into.</div>', unsafe_allow_html=True)
job_title = st.selectbox(
    "",
    options=[""] + JOB_TITLES,
    label_visibility="collapsed"
)

SKILLS_LIST = sorted([
    "Python", "SQL", "Spark", "PySpark", "Kafka", "Airflow", "dbt", "Snowflake",
    "Databricks", "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform",
    "Pandas", "Redshift", "BigQuery", "Looker", "Tableau", "Power BI",
    "LangChain", "LLM", "AI", "Machine Learning", "MLflow", "FastAPI",
    "Flask", "PostgreSQL", "MySQL", "MongoDB", "duckdb", "Polars",
    "Scikit-learn", "TensorFlow", "PyTorch", "Hugging Face", "OpenAI API",
    "Anthropic Claude", "Prompt Engineering", "RAG", "Vector Databases",
    "Dataiku", "Alteryx", "SAS", "R", "Scala", "Git", "CI/CD", "Collibra"
])

LOCATIONS = [
    "All US",
    "Remote",
    "New York, NY",
    "San Francisco, CA",
    "Seattle, WA",
    "Austin, TX",
    "Chicago, IL",
    "Boston, MA",
    "Los Angeles, CA",
    "Denver, CO",
    "Atlanta, GA",
    "Dallas, TX",
    "Washington, DC",
    "Miami, FL",
    "Minneapolis, MN",
    "Portland, OR",
    "San Diego, CA",
    "Phoenix, AZ",
    "Charlotte, NC",
    "Nashville, TN",
]

st.markdown('<div class="input-label">Location</div>', unsafe_allow_html=True)
st.markdown('<div class="input-hint">Select a city or search nationwide.</div>', unsafe_allow_html=True)
location_selection = st.selectbox(
    "",
    options=LOCATIONS,
    label_visibility="collapsed",
)
location = None if location_selection == "All US" else location_selection

if job_title:
    @st.cache_data(show_spinner=False)
    def get_salary_estimate(role, loc):
        return fetch_salary_estimate(role, loc)

    est = get_salary_estimate(job_title, location)
    if est:
        loc_label = location if location else "the US"
        st.markdown(
            f'<div class="rate-badge">💰 Market avg for <strong>{job_title}</strong> in {loc_label}: '
            f'~<strong>${est["avg"]:,}</strong> &nbsp;·&nbsp; range ${est["low"]:,} – ${est["high"]:,} '
            f'({est["count"]} postings)</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="input-label">Salary Range (USD / year)</div>', unsafe_allow_html=True)
st.markdown('<div class="input-hint">Filter jobs by salary. Drag to set your range.</div>', unsafe_allow_html=True)
salary_range = st.slider(
    "",
    min_value=40_000,
    max_value=300_000,
    value=(80_000, 200_000),
    step=5_000,
    format="$%d",
    label_visibility="collapsed",
)

st.markdown('<div class="input-label">Your Current Skills</div>', unsafe_allow_html=True)
st.markdown('<div class="input-hint">Search and select all that apply. No typos possible.</div>', unsafe_allow_html=True)
selected_skills = st.multiselect(
    "",
    options=SKILLS_LIST,
    placeholder="Search and select your skills...",
    label_visibility="collapsed"
)

remaining = MAX_REQUESTS - st.session_state.request_count
st.markdown(f'<div class="rate-badge">⚡ {remaining} of {MAX_REQUESTS} analyses remaining this session</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# BUTTON
if st.button("▶  Analyze My Market Position", type="primary", use_container_width=True):

    if not job_title or not selected_skills:
        st.warning("Please enter a role and select at least one skill.")

    elif st.session_state.request_count >= MAX_REQUESTS:
        st.error("You've used all 3 analyses for this session. Refresh the page to start over.")

    else:
        st.session_state.request_count += 1
        your_skills = [s.lower() for s in selected_skills]

        with st.spinner("Fetching live job postings..."):
            try:
                jobs = fetch_jobs(job_title, num_results=20, salary_min=salary_range[0], salary_max=salary_range[1], location=location or None)
            except Exception as e:
                st.error(f"API Error: {e}")
                st.stop()

        with st.spinner("Claude AI is reading job descriptions and extracting skills..."):
            try:
                skill_count = extract_skills_with_ai(jobs)
            except Exception as e:
                st.error(f"Skill extraction error: {e}")
                st.stop()

        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        total_jobs = len(jobs)

        salary_label = f"${salary_range[0]:,} - ${salary_range[1]:,}"
        location_label = location if location else "All US"
        st.markdown(f"""
        <div class="results-header">
            ✓ Analyzed {total_jobs} live job postings for <strong>{job_title}</strong> · {location_label} · Salary filter: {salary_label} · {len(skill_count)} unique skills detected by Claude AI
            <span style="float:right;font-size:0.68rem;opacity:0.5;font-weight:400;">via Adzuna Jobs API</span>
        </div>
        """, unsafe_allow_html=True)

        # Average salary from job results
        salaries = []
        for job in jobs:
            lo = job.get("salary_min")
            hi = job.get("salary_max")
            if lo and hi:
                salaries.append((lo + hi) / 2)
            elif lo:
                salaries.append(lo)
            elif hi:
                salaries.append(hi)

        if salaries:
            avg_salary = int(sum(salaries) / len(salaries))
            min_sal = int(min(salaries))
            max_sal = int(max(salaries))
            st.markdown(f"""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-left:3px solid #16a34a;border-radius:0 10px 10px 0;
                        padding:1rem 1.25rem;margin:0.75rem 0 1.25rem 0;">
                <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#15803d;margin-bottom:0.5rem;">
                    💰 Reported Salary — {job_title} · {location_label}
                </div>
                <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;color:#14532d;font-family:'DM Mono',monospace;">${avg_salary:,}</div>
                        <div style="font-size:0.72rem;color:#16a34a;text-transform:uppercase;letter-spacing:0.06em;">Avg salary</div>
                    </div>
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;color:#14532d;font-family:'DM Mono',monospace;">${min_sal:,}</div>
                        <div style="font-size:0.72rem;color:#16a34a;text-transform:uppercase;letter-spacing:0.06em;">Low</div>
                    </div>
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;color:#14532d;font-family:'DM Mono',monospace;">${max_sal:,}</div>
                        <div style="font-size:0.72rem;color:#16a34a;text-transform:uppercase;letter-spacing:0.06em;">High</div>
                    </div>
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;color:#14532d;font-family:'DM Mono',monospace;">{len(salaries)}</div>
                        <div style="font-size:0.72rem;color:#16a34a;text-transform:uppercase;letter-spacing:0.06em;">Jobs with salary data</div>
                    </div>
                </div>
                <div style="font-size:0.72rem;color:#86efac;margin-top:0.5rem;">Based on postings reporting salary within your filter range</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#94a3b8;font-size:0.82rem;margin-bottom:1rem;">No salary data reported in these postings.</p>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">🔥 Most In-Demand Skills Right Now</div>', unsafe_allow_html=True)
        for skill, count in sorted_skills[:12]:
            pct = int((count / max(total_jobs, 1)) * 100)
            st.markdown(f"""
            <div class="skill-bar-container">
                <div class="skill-bar-label">
                    <span class="skill-name">{skill}</span>
                    <span class="skill-count">{count} / {total_jobs} jobs ({pct}%)</span>
                </div>
                <div class="skill-bar-track">
                    <div class="skill-bar-fill" style="width:{pct}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        your_matched = [(s, c) for s, c in sorted_skills if s in your_skills]
        missing = [(s, c) for s, c in sorted_skills[:20] if s not in your_skills]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-title">✅ Skills You Already Have</div>', unsafe_allow_html=True)
            if your_matched:
                tags = "".join([f'<span class="tag-have">{s} · {c}</span>' for s, c in your_matched])
                st.markdown(f'<div class="tag-container">{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#94a3b8;font-size:0.82rem;">None matched in top skills</p>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-title">🚀 Top Gaps to Close</div>', unsafe_allow_html=True)
            if missing:
                tags = "".join([f'<span class="tag-missing">{s} · {c}</span>' for s, c in missing[:8]])
                st.markdown(f'<div class="tag-container">{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#94a3b8;font-size:0.82rem;">No major gaps found</p>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">🤖 Claude AI Career Assessment</div>', unsafe_allow_html=True)
        with st.spinner("Claude AI is generating your career assessment..."):
            advice = get_ai_advice(job_title, skill_count, your_skills)

        st.markdown(f'<div class="ai-advice-box">{advice}</div>', unsafe_allow_html=True)
        st.caption(f"Request {st.session_state.request_count} of {MAX_REQUESTS} used this session.")

        # Store results for download
        st.session_state.last_results = {
            "job_title": job_title,
            "total_jobs": total_jobs,
            "location": location_label,
            "salary_range": salary_range,
            "avg_salary": int(sum(salaries) / len(salaries)) if salaries else None,
            "min_salary": int(min(salaries)) if salaries else None,
            "max_salary": int(max(salaries)) if salaries else None,
            "salary_data_count": len(salaries),
            "sorted_skills": sorted_skills,
            "your_matched": your_matched,
            "missing": missing,
            "advice": advice,
        }

if "last_results" in st.session_state:
    r = st.session_state.last_results
    lines = [
        f"AI Career Advisor — Results Report",
        f"Generated: {__import__('datetime').date.today()}",
        f"Role: {r['job_title']}",
        f"Jobs Analyzed: {r['total_jobs']}",
        f"Location: {r['location']}",
        f"Salary Filter: ${r['salary_range'][0]:,} – ${r['salary_range'][1]:,}",
        f"Avg Reported Salary: ${r['avg_salary']:,}" if r['avg_salary'] else "Avg Reported Salary: No data",
        f"Salary Range (from postings): ${r['min_salary']:,} – ${r['max_salary']:,}" if r['avg_salary'] else "",
        "",
        "=== TOP IN-DEMAND SKILLS ===",
    ]
    for skill, count in r["sorted_skills"][:12]:
        pct = int((count / max(r["total_jobs"], 1)) * 100)
        lines.append(f"  {skill}: {count}/{r['total_jobs']} jobs ({pct}%)")
    lines += ["", "=== SKILLS YOU ALREADY HAVE ==="]
    for skill, count in r["your_matched"]:
        lines.append(f"  {skill} ({count} jobs)")
    lines += ["", "=== TOP GAPS TO CLOSE ==="]
    for skill, count in r["missing"][:8]:
        lines.append(f"  {skill} ({count} jobs)")
    lines += ["", "=== CLAUDE AI CAREER ASSESSMENT ===", r["advice"]]

    report = "\n".join(lines)
    st.download_button(
        label="⬇  Download Results as .txt",
        data=report,
        file_name=f"career_analysis_{r['job_title'].replace(' ', '_').lower()}.txt",
        mime="text/plain",
        use_container_width=True,
    )

# FOOTER
st.markdown("""
<div class="footer">
    Built by <a href="https://linkedin.com/in/vaishalizilpe" target="_blank">Vaishali Zilpe</a> · 
    <a href="https://github.com/vaishalizilpe/ai-skills-salary-advisor" target="_blank">View on GitHub</a> · 
    Powered by Adzuna Jobs API + Anthropic Claude
</div>
""", unsafe_allow_html=True)