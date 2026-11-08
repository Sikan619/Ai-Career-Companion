import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.ai_helper import extract_resume_details, is_groq_configured, PRIMARY_MODEL

st.set_page_config(page_title="Resume Analyzer | AI Career Companion", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.caption(f"Extract key skills, education, and experience from your PDF resume using AI • Model: **{PRIMARY_MODEL}**")

# Groq API status banner
if not is_groq_configured():
    st.info("💡 Note: Running in demo mode. Add your live `GROQ_API_KEY` to `.env` for full real-time cloud LLM extraction.")

# Initialize session state for extracted resume data
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "extracted_skills" not in st.session_state:
    st.session_state.extracted_skills = []

# Layout: File upload & Options
col_upload, col_info = st.columns([1.5, 1], gap="medium")

with col_upload:
    st.subheader("1. Upload Your Resume")
    uploaded_file = st.file_uploader("Upload resume in PDF format", type=["pdf"], help="Select a text-based PDF resume.")

    if uploaded_file is not None:
        try:
            with st.spinner("Reading PDF file with pdfplumber..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = extracted_text

            if extracted_text:
                st.success(f"✅ Successfully read **{uploaded_file.name}** ({len(extracted_text.split())} words)")
            else:
                st.warning("⚠️ No readable text found in this PDF. Please ensure it is not an image-only scanned document.")
        except Exception as e:
            st.error(f"Error parsing PDF file: {e}")

    # 1-Click Demo Sample Resume Loader (Great for live evaluation & viva)
    st.write("---")
    if st.button("📋 Or Load Demo Sample Resume (1-Click Test)", use_container_width=True):
        st.session_state.resume_text = """
Rahul Sharma
Email: rahul.sharma@example.com | Phone: +91 98765 43210 | Bangalore, India
LinkedIn: linkedin.com/in/rahul-sharma | GitHub: github.com/rahul-dev

EDUCATION
Bachelor of Computer Applications (BCA) - 2026
Christ University, Bangalore — CGPA: 8.7/10
Higher Secondary School (12th Standard - Science) — 89%

TECHNICAL SKILLS
Languages: Python, Java, JavaScript, SQL, HTML5, CSS3
Frameworks & Libraries: Streamlit, Django, Flask, Pandas, NumPy, React basics
Databases: PostgreSQL, MySQL, SQLite, MongoDB
Developer Tools: Git, GitHub, Docker, Postman, VS Code, Linux
Core Concepts: Data Structures & Algorithms, Object-Oriented Programming (OOP), RESTful APIs, DBMS

PROJECTS
1. AI Career Companion (Streamlit, Python, PostgreSQL, Groq LLM)
   - Developed a full-stack career platform to track job applications and automate resume analysis.
   - Integrated LLaMA-3.3 via Groq API for sub-second structured JSON resume parsing and cover letter generation.
   - Built dual-database fault-tolerant backend connecting to Cloud PostgreSQL with SQLite fallback.

2. Student Placement Portal (Django, PostgreSQL, Bootstrap)
   - Created role-based authentication for students and campus recruiters with automated eligibility filtering.

WORK EXPERIENCE / INTERNSHIPS
Software Development Intern — TechSolutions Inc. (Bangalore) | Jun 2025 - Dec 2025 (6 Months)
- Developed and consumed RESTful APIs for internal reporting tools using Python and PostgreSQL.
- Optimized database queries, reducing report generation latency by 28%.
- Collaborated in an Agile Scrum team with daily standups and Git version control.
"""
        st.success("✅ Demo sample resume loaded successfully! Click 'Extract Resume Details with AI' on the right to test.")

with col_info:
    st.subheader("2. Extraction Overview")
    st.write("Our AI will parse your document and extract:")
    st.markdown("- 🛠️ **Key Technical & Soft Skills**")
    st.markdown("- 🎓 **Education & Academic Background**")
    st.markdown("- 💼 **Professional Experience Summary**")
    st.markdown("- ⏳ **Estimated Total Years of Experience**")

    # Analyze Button
    if st.session_state.resume_text:
        analyze_clicked = st.button("✨ Extract Resume Details with AI", type="primary", use_container_width=True)
        if analyze_clicked:
            with st.spinner("AI is analyzing and extracting structured candidate details..."):
                try:
                    result = extract_resume_details(st.session_state.resume_text)
                    st.session_state.resume_data = result
                    st.session_state.extracted_skills = result.get("skills", [])
                    st.success("🎉 Resume analysis complete!")
                except Exception as ex:
                    st.error(f"Extraction failed: {ex}")

st.divider()

# Display Extracted Data
if st.session_state.resume_data:
    data = st.session_state.resume_data

    st.subheader("📊 Extracted Candidate Profile")

    # Metrics row for Total Experience
    exp_col, skills_count_col, edu_count_col = st.columns(3)
    exp_col.metric("⏳ Total Experience", data.get("total_experience_years", "Fresher / Entry-Level"))
    skills_count_col.metric("🛠️ Skills Detected", len(data.get("skills", [])))
    
    edu_list = data.get("education", [])
    edu_count_col.metric("🎓 Education Credentials", len(edu_list) if isinstance(edu_list, list) else 1)

    # Skills Section
    st.markdown("### 🛠️ Extracted Skills")
    skills = data.get("skills", [])
    if skills:
        # Display skills as modern tag pills
        badge_html = " ".join([
            f'<span style="display:inline-block; background-color:rgba(59, 130, 246, 0.15); color:#3b82f6; border:1px solid rgba(59, 130, 246, 0.35); border-radius:16px; padding:5px 14px; margin:4px 4px; font-size:14px; font-weight:600;">{skill}</span>'
            for skill in skills
        ])
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.write("No skills identified.")

    st.write("") # Spacing

    # Education and Experience Columns
    card_col1, card_col2 = st.columns(2, gap="medium")

    with card_col1:
        with st.container(border=True):
            st.markdown("#### 🎓 Education")
            if isinstance(edu_list, list) and edu_list:
                for item in edu_list:
                    st.markdown(f"- **{item}**")
            elif isinstance(edu_list, str):
                st.write(edu_list)
            else:
                st.write("No specific education detected.")

    with card_col2:
        with st.container(border=True):
            st.markdown("#### 💼 Experience Summary")
            st.write(data.get("experience_summary", "No experience summary available."))

    st.divider()

    # Next steps recommendation
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("🚀 Proceed to AI Assistant (Gap Analysis & Cover Letters)", type="primary", use_container_width=True):
            st.switch_page("pages/4_AI_Assistant.py")
    with c_btn2:
        with st.expander("🔍 View Raw Extracted Resume Text"):
            st.text_area("Plain Text", st.session_state.resume_text, height=250)

elif not st.session_state.resume_text:
    st.info("👆 Please upload a PDF resume above to see the AI extracted details.")
