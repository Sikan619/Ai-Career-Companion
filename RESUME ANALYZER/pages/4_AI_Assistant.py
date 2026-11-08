import streamlit as st
from utils.ai_helper import (
    generate_cover_letter,
    generate_followup_email,
    analyze_skills_gap,
    get_ai_response,
    is_groq_configured,
    PRIMARY_MODEL
)

st.set_page_config(page_title="AI Assistant | AI Career Companion", page_icon="🤖", layout="wide")

st.title("🤖 AI Career Assistant")
st.caption(f"Cover letter generator, follow-up emails, skills gap analysis, and interview advisor • Model: **{PRIMARY_MODEL}**")

# API status notice
if not is_groq_configured():
    st.info("💡 Note: Running with built-in intelligent offline templates. Add your live `GROQ_API_KEY` to `.env` for real-time cloud LLM generation.")

# Pre-fetch any skills extracted from the Resume Analyzer page
saved_skills = st.session_state.get("extracted_skills", [])
default_skills_str = ", ".join(saved_skills) if saved_skills else "Python, SQL, Problem Solving, Git"

# Tabs for the major AI capabilities
tab_cover, tab_email, tab_gap, tab_chat = st.tabs([
    "📝 Cover Letter Generator",
    "✉️ Follow-up Email Generator",
    "🎯 Skills Gap Analysis",
    "💬 Interactive Career Coach"
])

# ==========================================
# TAB 1: COVER LETTER GENERATOR
# ==========================================
with tab_cover:
    st.subheader("📝 Generate a Tailored Cover Letter")
    st.write("Craft a compelling, role-specific 3-paragraph cover letter highlighting your unique technical background.")

    if saved_skills:
        st.success(f"Loaded {len(saved_skills)} skills from your uploaded resume: **{', '.join(saved_skills[:6])}{'...' if len(saved_skills) > 6 else ''}**")

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        cl_company = st.text_input("Target Company Name *", placeholder="e.g. Infosys, TCS, Google, TechCorp", key="cl_comp")
        cl_role = st.text_input("Job Role Title *", placeholder="e.g. Associate Software Engineer, Data Analyst", key="cl_role")
    with c_col2:
        cl_skills = st.text_input("Candidate Key Skills", value=default_skills_str, help="Comma-separated skills to emphasize in the letter.")
        cl_jd = st.text_area("Job Description / Key Requirements (Optional)", placeholder="Paste key responsibilities or requirements to customize further...", height=68)

    if st.button("✨ Generate Professional Cover Letter", type="primary", use_container_width=True, key="btn_cl"):
        if not cl_company.strip() or not cl_role.strip():
            st.error("Please provide both Company Name and Job Role Title.")
        else:
            with st.spinner("AI is drafting your custom cover letter..."):
                try:
                    skills_list = [s.strip() for s in cl_skills.split(",") if s.strip()]
                    resume_context = st.session_state.get("resume_text", "")
                    cover_letter = generate_cover_letter(
                        user_skills=skills_list,
                        company=cl_company,
                        role=cl_role,
                        job_description=cl_jd,
                        resume_text=resume_context
                    )
                    st.session_state["generated_cover_letter"] = cover_letter
                    st.success("🎉 Cover Letter generated successfully!")
                except Exception as ex:
                    st.error(f"Error generating cover letter: {ex}")

    # Display generated cover letter if present
    if "generated_cover_letter" in st.session_state and st.session_state["generated_cover_letter"]:
        st.divider()
        st.subheader("📄 Your Tailored Cover Letter")
        st.text_area("Cover Letter Text", value=st.session_state["generated_cover_letter"], height=320)
        
        st.download_button(
            label="📥 Download Cover Letter (.txt)",
            data=st.session_state["generated_cover_letter"],
            file_name=f"Cover_Letter_{cl_company or 'Application'}.txt",
            mime="text/plain"
        )

# ==========================================
# TAB 2: FOLLOW-UP EMAIL GENERATOR
# ==========================================
with tab_email:
    st.subheader("✉️ Generate Professional Follow-up Emails")
    st.write("Generate polite, impactful post-interview thank you notes and application status check-in emails.")

    em_col1, em_col2 = st.columns(2)
    with em_col1:
        email_type = st.selectbox(
            "Email Scenario / Purpose",
            [
                "Post-Interview Thank You",
                "Application Status Follow-up",
                "Offer / Decision Follow-up"
            ]
        )
        em_company = st.text_input("Company Name", placeholder="e.g. Wipro, Amazon, Innovate Inc.", key="em_comp")
    with em_col2:
        em_role = st.text_input("Job Role Title", placeholder="e.g. Python Developer, Junior Data Scientist", key="em_role")
        em_interviewer = st.text_input("Interviewer / Recruiter Name (Optional)", placeholder="e.g. Sarah Jenkins or Hiring Team", key="em_person")

    em_notes = st.text_input(
        "Key Topic Discussed or Note (Optional)",
        placeholder="e.g. enjoyed our conversation about cloud migrations and microservices",
        key="em_note"
    )

    if st.button("✨ Draft Follow-up Email", type="primary", use_container_width=True, key="btn_em"):
        with st.spinner("AI is composing your follow-up email..."):
            try:
                email_text = generate_followup_email(
                    email_type=email_type,
                    company=em_company,
                    role=em_role,
                    interviewer_name=em_interviewer,
                    notes=em_notes
                )
                st.session_state["generated_email"] = email_text
                st.success("🎉 Email drafted successfully!")
            except Exception as ex:
                st.error(f"Error drafting email: {ex}")

    if "generated_email" in st.session_state and st.session_state["generated_email"]:
        st.divider()
        st.subheader("📬 Generated Follow-up Email")
        st.text_area("Email Content", value=st.session_state["generated_email"], height=250)
        
        st.download_button(
            label="📥 Download Email Draft (.txt)",
            data=st.session_state["generated_email"],
            file_name=f"Email_{email_type.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# ==========================================
# TAB 3: SKILLS GAP ANALYSIS
# ==========================================
with tab_gap:
    st.subheader("🎯 Skills Gap Analysis")
    st.write("Compare your current skills against the job requirements to calculate your match score and identify missing areas.")

    gap_col1, gap_col2 = st.columns(2)
    with gap_col1:
        st.markdown("#### 1. Your Current Skills")
        user_skills_input = st.text_area(
            "Enter your skills (comma-separated)",
            value=default_skills_str,
            height=130,
            help="Skills loaded automatically from your resume, or entered manually."
        )
    with gap_col2:
        st.markdown("#### 2. Target Job Requirements")
        jd_input = st.text_area(
            "Paste Job Description / Required Skills *",
            placeholder="e.g. Required: Python, SQL, Docker, FastAPI, AWS, CI/CD, Git. Good to have: React, Redis...",
            height=130
        )

    if st.button("🔍 Perform Skills Gap Analysis", type="primary", use_container_width=True, key="btn_gap"):
        if not jd_input.strip():
            st.error("Please paste the Target Job Description or Required Skills.")
        else:
            with st.spinner("Analyzing skills alignment and calculating match score..."):
                try:
                    skills_list = [s.strip() for s in user_skills_input.split(",") if s.strip()]
                    gap_result = analyze_skills_gap(skills_list, jd_input)
                    st.session_state["gap_result"] = gap_result
                    st.success("🎉 Analysis complete!")
                except Exception as ex:
                    st.error(f"Gap analysis failed: {ex}")

    # Display Gap Analysis Results
    if "gap_result" in st.session_state and st.session_state["gap_result"]:
        res = st.session_state["gap_result"]
        st.divider()

        score = res.get("match_score", 0)
        
        # Match Score Display
        score_col, note_col = st.columns([1, 2])
        with score_col:
            st.metric("🎯 ATS / Role Match Score", f"{score}%")
            st.progress(score / 100.0)
        with note_col:
            if score >= 75:
                st.success("🌟 **Strong Match!** You meet most of the core technical qualifications for this position.")
            elif score >= 50:
                st.warning("⚡ **Moderate Match.** You have foundational skills, but adding a few missing keywords will boost your chances.")
            else:
                st.error("⚠️ **Significant Gap.** Consider building a targeted project covering the missing requirements.")

        st.write("")

        # Matching vs Missing Skills
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            with st.container(border=True):
                st.markdown("#### ✅ Matching Skills You Have")
                matching = res.get("matching_skills", [])
                if matching:
                    for s in matching:
                        st.markdown(f"- **{s}**")
                else:
                    st.write("No direct keyword matches found.")

        with m_col2:
            with st.container(border=True):
                st.markdown("#### ⚠️ Missing / Recommended Skills")
                missing = res.get("missing_skills", [])
                if missing:
                    for m in missing:
                        st.markdown(f"- <span style='color:#dc2626; font-weight:600;'>{m}</span>", unsafe_allow_html=True)
                else:
                    st.write("No major skill gaps identified!")

        # Recommendations Card
        with st.container(border=True):
            st.markdown("#### 💡 Actionable Improvement Roadmap")
            st.write(res.get("recommendations", "Review the required technologies and build portfolio projects."))

# ==========================================
# TAB 4: INTERACTIVE CAREER COACH
# ==========================================
with tab_chat:
    st.subheader("💬 AI Interview & Career Coach")
    st.write("Get real-time answers for interview questions, behavioral scenarios (STAR method), and career advice.")

    # Initialize chat history
    if "coach_messages" not in st.session_state:
        st.session_state.coach_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am your AI Career Advisor. Ask me anything about behavioral questions, technical interviews, resume tips, or salary negotiation!"
            }
        ]

    # Quick prompt shortcuts
    st.markdown("**Quick Prompts:**")
    p1, p2, p3, p4 = st.columns(4)
    quick_selected = None
    if p1.button("🎯 STAR Method Tips", use_container_width=True):
        quick_selected = "Explain the STAR method for answering behavioral interview questions with an example."
    if p2.button("💰 Salary Negotiation", use_container_width=True):
        quick_selected = "What are the best tips to negotiate my first job offer professionally?"
    if p3.button("❓ Questions for Interviewer", use_container_width=True):
        quick_selected = "What are the top 5 thoughtful questions to ask the interviewer at the end of an interview?"
    if p4.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.coach_messages = [
            {"role": "assistant", "content": "Chat cleared! How can I assist you next?"}
        ]
        st.rerun()

    # Display conversation history
    for msg in st.session_state.coach_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle chat input
    user_input = st.chat_input("Ask a career or interview question...")
    if quick_selected:
        user_input = quick_selected

    if user_input:
        st.session_state.coach_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                try:
                    system_msg = {
                        "role": "system",
                        "content": "You are an encouraging, experienced career counselor and interview coach. Give clear, structured, and actionable advice with bullet points."
                    }
                    messages_to_send = [system_msg] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.coach_messages
                    ]
                    reply = get_ai_response(messages_to_send)
                    st.markdown(reply)
                    st.session_state.coach_messages.append({"role": "assistant", "content": reply})
                except Exception as ex:
                    err_text = f"⚠️ Could not reach AI service: {ex}"
                    st.error(err_text)
                    st.session_state.coach_messages.append({"role": "assistant", "content": err_text})
