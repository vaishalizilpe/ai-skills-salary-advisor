import streamlit as st
import os
from job_fetcher import fetch_jobs, extract_skills
from ai_advisor import get_ai_advice

# Page config
st.set_page_config(
    page_title="AI Skills & Salary Advisor",
    page_icon="🤖",
    layout="centered"
)

# Header
st.title("🤖 AI Skills & Salary Advisor")
st.markdown("Find out what the job market wants right now — and get AI-powered advice on what to learn next.")
st.divider()

# User inputs
job_title = st.text_input(
    "What role are you targeting?",
    placeholder="e.g. Data Engineer, Analytics Engineer, AI Engineer"
)

your_skills_input = st.text_area(
    "What are your current skills? (comma separated)",
    placeholder="e.g. SQL, Python, dbt, Snowflake, Tableau"
)

# Run button
if st.button("Get My AI Career Advice", type="primary"):

    if not job_title or not your_skills_input:
        st.warning("Please fill in both fields above.")
    else:
        your_skills = [s.strip().lower() for s in your_skills_input.split(",")]

        # Fetch jobs
        with st.spinner("Fetching live job market data..."):
            jobs = fetch_jobs(job_title, num_results=20)
            skill_count = extract_skills(jobs)

        # Show market insights
        st.subheader("🔥 Most In-Demand Skills Right Now")
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)

        for skill, count in sorted_skills[:10]:
            st.progress(count / 20, text=f"{skill} — {count} jobs")

        st.divider()

        # Show skill gap
        your_matched = [(s, c) for s, c in sorted_skills if s in your_skills]
        missing = [(s, c) for s, c in sorted_skills[:15] if s not in your_skills]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Your Matched Skills")
            for skill, count in your_matched:
                st.success(f"{skill} — {count} jobs")

        with col2:
            st.subheader("🚀 Skills to Learn Next")
            for skill, count in missing[:5]:
                st.info(f"{skill} — {count} jobs")

        st.divider()

        # AI advice
        st.subheader("🤖 Your Personal AI Career Advisor")
        with st.spinner("Claude AI is analyzing your profile..."):
            advice = get_ai_advice(job_title, skill_count, your_skills)

        st.markdown(advice)