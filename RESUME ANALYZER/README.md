# 💼 AI Career Companion

> **Your smart, all-in-one personal job hunting assistant that organizes your applications, reads your resume, finds missing skills, and writes custom cover letters in seconds.**

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)](https://neon.tech/)
[![Groq LLaMA 3.3](https://img.shields.io/badge/AI%20Engine-Groq%20LLaMA--3.3-F05A28)](https://groq.com/)
[![Python](https://img.shields.io/badge/Language-Python%203.10+-3776AB?logo=python&logoColor=white)](https://python.org/)

---

## 🌟 What is AI Career Companion? (In Simple Words)

Searching for jobs and campus placements is stressful. Most students and job seekers have to:
- 😫 Manage messy spreadsheets to remember where they applied and when interviews are scheduled.
- 🤔 Wonder why they aren't getting interview calls or what skills are missing from their resume.
- ⏳ Spend hours writing the same cover letters and follow-up emails from scratch.

**AI Career Companion fixes all of that.** 

Think of it as your **personal career assistant** that lives in your web browser:
1. **No More Messy Spreadsheets:** Track every job you apply for in a clean dashboard with visual charts that show your progress (*Applied*, *Interview*, *Offer*).
2. **Instant Resume Reader:** Simply drop your PDF resume into the app. The AI reads it in seconds and neatly lists your technical skills, education, and years of experience.
3. **Smart Job Matcher (Skills Gap Analysis):** Paste any job description, and the AI tells you: *"You are an 80% match! You have Python and SQL, but you should learn Docker and AWS to get this job."*
4. **1-Click Writing Assistant:** Generates tailored, professional **Cover Letters** and post-interview **Thank-You Emails** ready to send with one click.

---

## 🚀 Key Features

### 1. 📊 Visual Job Application Tracker
- Replace Google Sheets with a dedicated, interactive dashboard.
- Live progress metrics: Total Applications, Pending Reviews, Scheduled Interviews, and Job Offers.
- Interactive charts (status breakdown donut chart & applications timeline).
- Search by company name or role, filter by status, and export your entire pipeline to CSV spreadsheet.

### 2. 📄 AI Resume Analyzer
- Upload any text-based PDF resume.
- Automatically extracts your **Skills**, **Education**, and **Experience Summary** into interactive visual badges.
- Keeps extracted skills saved in memory so you don't have to retype them on other pages!
- Includes a **1-Click Demo Resume** button so anyone can test it instantly without needing a PDF file.

### 3. 🎯 Skills Gap Analysis
- Compare your resume skills directly against any job description.
- Get a realistic **ATS / Role Match Score (0–100%)**.
- Shows clear columns for **Matching Skills You Have** vs **Missing Keywords to Learn**.
- Provides an actionable learning roadmap to help you bridge the gap before the interview.

### 4. 📝 1-Click Cover Letter & Email Generator
- **Custom Cover Letters:** Writes tailored, polite 3-paragraph letters highlighting your exact skills for the target company.
- **Follow-up Emails:** Prepares professional emails for post-interview thank yous, checking on application status, and offer follow-ups.
- **Download Ready:** Download your letters as clean `.txt` files with 1 click.

### 5. 🛡️ Never-Crash Database Architecture
- Connects automatically to **Cloud PostgreSQL (Neon.tech)** for secure, real-time data storage.
- If internet is unavailable or cloud database is offline, it automatically falls back to a **local SQLite database** so the app **never crashes** during live presentations.

---

## 🛠️ Tech Stack (Under the Hood)

- **Frontend:** [Streamlit](https://streamlit.io/) (Multi-page reactive web app)
- **Database:** Cloud PostgreSQL ([Neon.tech](https://neon.tech/)) with local SQLite fallback
- **Database Driver:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Secure parameterized queries, zero SQL injection)
- **AI / LLM:** [Groq Cloud](https://groq.com/) running Meta's `llama-3.3-70b-versatile` (Sub-second inference speeds)
- **PDF Extraction:** [pdfplumber](https://github.com/jsvine/pdfplumber)
- **Charts:** Plotly Express & Pandas
- **Styling:** Custom CSS supporting both **Dark Mode** and **Light Mode** seamlessly

---

## 🏃 Quick Start Guide

### 1. Clone this repository
```bash
git clone https://github.com/your-username/ai-career-companion.git
cd ai-career-companion
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```ini
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
GROQ_API_KEY=gsk_your_groq_api_key_here
```
*(Note: If you don't have an API key yet, the app runs smoothly in **Demo Mode** using intelligent built-in templates!)*

### 4. Launch the application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser!

---

## 📁 Project Structure

```
ai-career-companion/
├── app.py                                # Main home page & live pipeline metrics
├── requirements.txt                      # Python dependencies
├── .env                                  # Database & AI credentials
├── README.md                             # Project documentation
├── INTERVIEW_PREP_AND_PROJECT_GUIDE.txt  # Complete viva / interview guide with 30 Q&As
├── assets/
│   └── style.css                         # Dark/Light theme-aware styling
├── data/
│   └── career_companion.db               # Local SQLite database (automatic fallback)
├── pages/
│   ├── 1_Dashboard.py                    # Analytics, search/filter, CSV export, CRUD
│   ├── 2_Add_Application.py              # Log new job applications
│   ├── 3_Resume_Analyzer.py              # PDF resume upload & AI skill extraction
│   └── 4_AI_Assistant.py                 # Cover letters, emails & skills gap analysis
└── utils/
    ├── database.py                       # PostgreSQL + SQLite dual-engine database layer
    ├── ai_helper.py                      # Groq LLM integration & offline fallback logic
    ├── resume_parser.py                  # pdfplumber text extraction
    └── charts.py                         # Theme-aware Plotly charts
```

---

## 🎓 About This Project
Developed by a **BCA final year student** as a practical placement project to demonstrate full-stack Python development, relational database integration, and modern Generative AI engineering.
