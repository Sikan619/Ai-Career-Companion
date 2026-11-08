import streamlit as st
from utils.database import add_application, DB_TYPE
from datetime import date

st.set_page_config(page_title="Add Application | AI Career Companion", page_icon="➕", layout="wide")

st.title("➕ Add New Job Application")
st.caption(f"Log a new role in your job hunt pipeline • Database: **{DB_TYPE}**")

# Container for clean card styling
with st.container(border=True):
    with st.form("application_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("Company Name *", placeholder="e.g. Google, Infosys, Amazon, Startup Inc.")
            role = st.text_input("Job Role *", placeholder="e.g. Software Engineer, Full Stack Developer, Data Analyst")
            status = st.selectbox(
                "Application Status",
                ["Applied", "Interview", "Offer", "Rejected", "Wishlist"],
                index=0
            )

        with col2:
            applied_date = st.date_input("Applied Date", value=date.today())
            job_link = st.text_input("Job / Career Portal Link (optional)", placeholder="https://careers.company.com/job/...")
            notes = st.text_area("Notes & Interview Details (optional)", placeholder="Referral name, salary range, recruiter contact, test date...", height=105)

        st.caption("* Required fields")
        submitted = st.form_submit_button("🚀 Submit & Save Application", type="primary", use_container_width=True)

        if submitted:
            if company.strip() and role.strip():
                try:
                    add_application(
                        company=company.strip(),
                        role=role.strip(),
                        status=status,
                        applied_date=applied_date,
                        job_link=job_link.strip(),
                        notes=notes.strip()
                    )
                    st.success(f"✅ Successfully added application for **{role.strip()}** at **{company.strip()}**!")
                except Exception as e:
                    st.error(f"Failed to save application: {e}")
            else:
                st.error("⚠️ Please fill in both **Company Name** and **Job Role**.")

st.divider()

# Navigation helper buttons
nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("📊 View All Applications on Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
with nav_col2:
    if st.button("📄 Analyze Resume & Check Skills", use_container_width=True):
        st.switch_page("pages/3_Resume_Analyzer.py")
