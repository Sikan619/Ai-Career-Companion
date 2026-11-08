# 💼 AI Career Companion

### Your AI-Powered Placement Co-Pilot & Job Application Tracker

An all-in-one career management platform designed to help students and job seekers organize their job applications, analyze resumes, identify skill gaps, and prepare professional application documents.

AI Career Companion combines application tracking, resume intelligence, and AI-powered career assistance in one unified dashboard.

---

## 🚀 Key Features

### 1. 📊 Job Application Dashboard

- Track all job applications in one place.
- Monitor application progress and hiring status.
- Visualize application statistics through interactive charts.
- Analyze application trends over time.
- View interviews, offers, pending applications, and rejections.

### 2. 📝 Application Management System

- Add new job applications with company and role details.
- Edit and delete existing application records.
- Track application dates and hiring status.
- Store job links and additional notes.
- Search applications by company or job role.
- Filter applications by status.
- Export application records as CSV reports.

### 3. 📄 AI Resume Analyzer

- Upload resumes in PDF format.
- Extract key technical and soft skills.
- Identify educational qualifications.
- Summarize professional experience.
- Estimate total years of experience.
- View structured resume extraction results.

### 4. 🤖 AI Career Assistant

The platform provides four career assistance modules:

| Module                    | Functionality                                            |
| ------------------------- | -------------------------------------------------------- |
| Cover Letter Generator    | Generates role-specific professional cover letters.      |
| Follow-up Email Generator | Helps prepare professional recruitment follow-up emails. |
| Skills Gap Analysis       | Compares candidate skills against job requirements.      |
| Interactive Career Coach  | Provides career-related guidance and assistance.         |

### 5. 🗄️ Cloud Database

- PostgreSQL database integration.
- Neon Cloud PostgreSQL hosting.
- Persistent storage for job application records.

---

## 🛠️ Technology Stack

| Category             | Technologies            |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Frontend / UI        | Streamlit               |
| Database             | PostgreSQL              |
| Cloud Database       | Neon                    |
| AI Integration       | Groq API                |
| Language Model       | Llama 3.3 70B Versatile |
| Document Processing  | PDF resume extraction   |
| Data Visualization   | Interactive charts      |
| Data Export          | CSV                     |

---

## 🏗️ System Architecture

The application follows a modular architecture connecting the user interface, database, and AI services.
```
                 USER
                   |
                   v
          STREAMLIT INTERFACE
                   |
          +--------+---------+
          |                  |
          v                  v
    APPLICATION          AI CAREER
     TRACKING              TOOLS
          |                  |
          v          +-------+-------+
     PYTHON LOGIC    |       |       |
          |          v       v       v
          v        Resume  Skills  Content
     PostgreSQL    Analysis Gap    Generation
       (Neon)        |     Analysis    |
          |          +-------+---------+
          |                  |
          v                  v
     Application          Groq API
       Records          / Demo Mode
```

---

## ⚙️ AI Integration

The AI modules are designed around the Groq API and the Llama 3.3 70B Versatile model.

**Current implementation status:**

- Demo mode: Built-in offline templates are available.
- Live AI mode: Requires a valid Groq API key.
- Resume analysis: Supports a demo sample and PDF upload interface.
- AI career assistance: Provides the four career tools through the application interface.

To enable live AI generation, configure your Groq API key using an environment variable.
```
GROQ_API_KEY=your_groq_api_key
```

Never commit your actual API key or database credentials to GitHub.

---

## 📸 Application Preview

The application includes the following interfaces:

| Interface           | Description                                |
| ------------------- | ------------------------------------------ |
| Main Dashboard      | Application overview and navigation        |
| Job Tracking        | Application records and pipeline analytics |
| Add Application     | New job application form                   |
| Resume Analyzer     | PDF resume upload and extraction           |
| AI Career Assistant | AI-powered career generation tools         |

*Add your application screenshots to a `docs/screenshots/` directory and link them here.*

---

## 💻 Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL database
- Neon PostgreSQL account (for cloud database usage)
- Groq API key (for live AI functionality)
- Git

### Installation

**1. Clone the repository**
```
git clone https://github.com/Sikan619/AI-Career-Companion.git
```

**2. Navigate to the project directory**
```
cd AI-Career-Companion
```

**3. Create a virtual environment**
```
python -m venv venv
```

**4. Activate the environment**

Windows:
```
venv\Scripts\activate
```

Linux / macOS:
```
source venv/bin/activate
```

**5. Install dependencies**

Install the packages listed in the project's requirements file.

**6. Configure environment variables**

Create a `.env` file and configure your Groq API key and PostgreSQL connection settings according to the application's configuration.

**7. Run the application**

Launch the Streamlit application using its main entry-point file.

> Note: Confirm the actual requirements file location and Streamlit entry-point filename in the project before running these steps.

---

## 🔐 Security Considerations

- Keep API keys in environment variables.
- Never upload `.env` files containing credentials.
- Protect PostgreSQL connection credentials.
- Avoid committing personal resume documents.
- Use `.gitignore` to exclude sensitive files.

---

## 🎯 Project Objectives

This project aims to solve common job-search management problems faced by college students and fresh graduates.

It focuses on:

- Simplifying job application tracking.
- Reducing repetitive application documentation work.
- Making resume information easier to understand.
- Identifying skill gaps before applying for jobs.
- Helping students prepare professional communication.
- Bringing essential placement tools into one platform.

---

## 🔮 Future Enhancements

- Automated job discovery and job matching.
- Resume-to-job-description compatibility scoring.
- Advanced interview preparation with AI feedback.
- Personalized learning roadmaps for missing skills.
- Application deadline notifications.
- Application analytics and performance insights.
- Improved authentication and multi-user support.

---

## 👨‍💻 Developer

**SIKON KUMAR PANDA**

BCA Student | Python & Database Development | AI-Powered Applications

Interested in software engineering, backend development, database systems, and practical AI applications.

---

## 📜 License

This project is distributed under the license available in the repository's `LICENSE` file.

---

⭐ If you find this project interesting, consider giving the repository a star!

**AI Career Companion | Making the Job Search Journey Smarter.**



EYY LE AUR ADD KAR JO KARNA HAI
