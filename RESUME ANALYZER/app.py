import os
import pathlib
import streamlit as st
from utils.database import init_db, get_all_applications, DB_TYPE
from utils.ai_helper import is_groq_configured, PRIMARY_MODEL

st.set_page_config(
    page_title="AI Career Companion",
    page_icon="💼",
    layout="wide"
)

# Load custom CSS styling if available
css_path = pathlib.Path(__file__).resolve().parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize database tables
try:
    init_db()
except Exception as e:
    st.error(f"Database initialization warning: {e}")

# Main Header
st.title("💼 AI Career Companion")
st.markdown("##### *Your All-in-One AI-Powered Placement Co-Pilot & Job Application Tracker*")

# System Status Pills
db_badge_color = "#10b981" if "Cloud" in DB_TYPE else "#f59e0b"
groq_ready = is_groq_configured()
ai_badge_color = "#10b981" if groq_ready else "#6b7280"
ai_status_text = f"Connected ({PRIMARY_MODEL})" if groq_ready else "Demo Mode (Offline Templates)"

st.markdown(
    f"""
    <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
        <span class="status-pill">
            🗄️ <strong>Database:</strong> <span style="color: {db_badge_color}; font-weight: 600;">{DB_TYPE}</span>
        </span>
        <span class="status-pill">
            🤖 <strong>AI Engine:</strong> <span style="color: {ai_badge_color}; font-weight: 600;">{ai_status_text}</span>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Welcome to **AI Career Companion**! Built specifically for college students and job seekers to streamline "
    "their placement drive journey: track every application, extract resume skills with AI, perform real-time "
    "skills gap analysis against job descriptions, and generate tailored cover letters and follow-up emails in seconds."
)

st.divider()

# Live Application Pipeline Metrics
try:
    applications = get_all_applications()
    total_apps = len(applications)
    interviews = sum(1 for app in applications if app.get("status", "").lower() == "interview")
    offers = sum(1 for app in applications if app.get("status", "").lower() == "offer")
    pending = sum(1 for app in applications if app.get("status", "").lower() == "applied")
except Exception:
    total_apps = 0
    interviews = 0
    offers = 0
    pending = 0

st.subheader("📊 Your Job Search At A Glance")
m1, m2, m3, m4 = st.columns(4)
m1.metric("📋 Total Applications", total_apps)
m2.metric("⏳ In Review / Applied", pending)
m3.metric("🎯 Interviews Scheduled", interviews)
m4.metric("🎉 Job Offers", offers)

st.divider()

# Quick Navigation Cards
st.subheader("🚀 Platform Features & Navigation")

col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.markdown("### 📊 Application Tracking")
        st.write("Keep your entire placement pipeline organized with full CRUD controls, status management, and interactive analytics.")
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("➕ Add Application", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Add_Application.py")
        with btn_c2:
            if st.button("📈 View Dashboard", use_container_width=True):
                st.switch_page("pages/1_Dashboard.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🤖 AI Career Tools")
        st.write("Extract skills and credentials from your PDF resume, calculate job match scores, and draft professional outreach emails.")
        
        btn_c3, btn_c4 = st.columns(2)
        with btn_c3:
            if st.button("📄 Resume Analyzer", use_container_width=True, type="primary"):
                st.switch_page("pages/3_Resume_Analyzer.py")
        with btn_c4:
            if st.button("💬 AI Assistant Suite", use_container_width=True):
                st.switch_page("pages/4_AI_Assistant.py")

st.divider()

# Technical Architecture Info (Great for Viva & Project Evaluation)
with st.expander("ℹ️ About Project Architecture & Technologies (BCA Final Year / Placement Project)"):
    st.markdown("""
    - **Frontend:** Streamlit Multi-Page Web Architecture with Custom CSS
    - **Database:** Cloud PostgreSQL (Neon.tech) with automatic fault-tolerant SQLite fallback
    - **Database Driver:** SQLAlchemy 2.0 with connection pooling
    - **AI / LLM:** Groq High-Speed Inference Cloud (`llama-3.3-70b-versatile` & `llama-3.1-8b-instant`)
    - **PDF Extraction:** `pdfplumber` byte-stream parser
    - **Data Analytics:** Pandas & Plotly Express interactive charts
    - **Security:** Environment variable management via `python-dotenv`
    """)

st.caption("AI Career Companion © 2026 • Designed for smooth college placement & job hunt tracking.")
