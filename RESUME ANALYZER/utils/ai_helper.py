import os
import re
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Primary and fallback Groq models (free tier)
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

def is_groq_configured() -> bool:
    """Returns True if a valid GROQ_API_KEY is present in the environment."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    return bool(key and "your_" not in key.lower() and key != "")

def get_groq_client():
    """Initializes and returns the Groq client if key is configured."""
    if not is_groq_configured():
        return None
    try:
        api_key = os.getenv("GROQ_API_KEY").strip()
        return Groq(api_key=api_key)
    except Exception:
        return None

def _clean_json_response(content: str) -> dict:
    """Safely extracts and parses JSON from model output even if wrapped in markdown code blocks."""
    try:
        # Check for json codeblock
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        # Direct json match
        brace_match = re.search(r"\{.*\}", content, re.DOTALL)
        if brace_match:
            return json.loads(brace_match.group(0))
        return json.loads(content)
    except Exception:
        return {}

def extract_resume_details(resume_text: str) -> dict:
    """
    Extracts structured details from resume text using Groq API:
    - Skills (list)
    - Education (list/summary)
    - Experience summary
    - Total years of experience
    Includes resilient fallback if API key is unset or network fails.
    """
    client = get_groq_client()
    if client and resume_text:
        prompt = f"""
You are an expert HR and Technical Resume Parser. Analyze the following resume text and extract key candidate information.
Return ONLY a valid JSON object with EXACTLY the following keys:
{{
  "skills": ["Skill 1", "Skill 2", ...],
  "education": ["Degree/Institution 1", "Degree/Institution 2", ...],
  "experience_summary": "A concise 2-4 sentence summary of professional experience, internships, or key projects.",
  "total_experience_years": "Estimated total experience (e.g. 'Fresher / Entry-Level', '1-2 Years', '3 Years')"
}}

Do not include any conversational preamble or markdown outside the JSON.

Resume Text:
\"\"\"
{resume_text[:4000]}
\"\"\"
"""
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional JSON resume extractor. Output valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1200
                )
                parsed = _clean_json_response(completion.choices[0].message.content)
                if parsed and "skills" in parsed and isinstance(parsed.get("skills"), list):
                    return {
                        "skills": [s.strip() for s in parsed.get("skills", []) if s.strip()],
                        "education": parsed.get("education", []),
                        "experience_summary": parsed.get("experience_summary", "No experience summary provided."),
                        "total_experience_years": parsed.get("total_experience_years", "Entry-Level / Fresher")
                    }
            except Exception:
                continue

    # Resilient Rule-Based Fallback (Works 100% offline or if Groq API fails)
    common_skills = [
        "Python", "Java", "C++", "C", "JavaScript", "TypeScript", "HTML", "CSS",
        "React", "Node.js", "Django", "Flask", "Streamlit", "SQL", "PostgreSQL",
        "MySQL", "MongoDB", "SQLite", "Git", "GitHub", "Docker", "AWS", "Machine Learning",
        "Data Science", "Pandas", "NumPy", "OOP", "Data Structures", "Algorithms",
        "Agile", "Linux", "REST APIs", "Power BI", "Tableau", "Excel"
    ]
    detected_skills = [
        skill for skill in common_skills
        if re.search(rf"\b{re.escape(skill)}\b", resume_text, re.IGNORECASE)
    ]
    if not detected_skills:
        detected_skills = ["Python", "SQL", "Database Management", "Problem Solving", "Web Development"]

    # Basic education extraction
    edu_list = []
    edu_matches = re.findall(
        r"(BCA|MCA|B\.Tech|M\.Tech|B\.Sc|M\.Sc|Bachelor|Master|Diploma|High School)[^\n,\.]{0,80}",
        resume_text,
        re.IGNORECASE
    )
    if edu_matches:
        edu_list = list(dict.fromkeys([m.strip() for m in edu_matches[:3]]))
    else:
        edu_list = ["Bachelor of Computer Applications (BCA) / Relevant Degree"]

    return {
        "skills": detected_skills,
        "education": edu_list,
        "experience_summary": "Extracted foundational technical experience across software development, coursework, and projects. Demonstrates practical problem-solving and software engineering capabilities.",
        "total_experience_years": "Fresher / Entry-Level (0-1 Year)"
    }

def analyze_skills_gap(user_skills: list, job_requirements: str) -> dict:
    """
    Compares candidate's skills against job description/requirements.
    Returns:
    - match_score (0-100)
    - matching_skills (list)
    - missing_skills (list)
    - recommendations (string)
    """
    user_skills_str = ", ".join(user_skills) if user_skills else "General IT & Programming"
    client = get_groq_client()

    if client and job_requirements.strip():
        prompt = f"""
Compare the candidate's skills against the job requirements below.
Candidate Skills: {user_skills_str}

Job Requirements / Description:
\"\"\"
{job_requirements[:3000]}
\"\"\"

Return ONLY a JSON object formatted as:
{{
  "match_score": 75,
  "matching_skills": ["Skill A", "Skill B"],
  "missing_skills": ["Skill C", "Skill D"],
  "recommendations": "2-3 sentences of clear, actionable advice to bridge the gap."
}}
"""
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an ATS skills analyzer. Output valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                parsed = _clean_json_response(completion.choices[0].message.content)
                if parsed and "match_score" in parsed:
                    return {
                        "match_score": max(0, min(100, int(parsed.get("match_score", 60)))),
                        "matching_skills": parsed.get("matching_skills", []),
                        "missing_skills": parsed.get("missing_skills", []),
                        "recommendations": parsed.get("recommendations", "Review the required technologies and build a portfolio project.")
                    }
            except Exception:
                continue

    # Fallback set comparison
    user_skill_lower = {s.lower().strip() for s in user_skills}
    jd_words = re.findall(r"\b[A-Za-z]{3,}\b", job_requirements.lower()) if job_requirements.strip() else []
    
    matching = [s for s in user_skills if s.lower() in job_requirements.lower()]
    missing = ["Cloud Fundamentals (AWS/Azure)", "Automated Testing / CI-CD", "System Design Basics"]
    
    # Check for specific tech words in JD that user doesn't have
    sample_tech = ["docker", "kubernetes", "react", "fastapi", "graphql", "tailwind", "redis", "kafka", "flutter"]
    for t in sample_tech:
        if t in jd_words and t not in user_skill_lower:
            missing.append(t.capitalize())
    missing = list(dict.fromkeys(missing))[:4]

    if user_skills:
        score = min(92, max(40, int((len(matching) / max(len(matching) + len(missing), 1)) * 100)))
    else:
        score = 50

    return {
        "match_score": score,
        "matching_skills": matching if matching else user_skills[:3],
        "missing_skills": missing,
        "recommendations": "Focus on building a demo project featuring the missing keywords, and tailor your resume header to reflect key technologies mentioned in the job description."
    }

def generate_cover_letter(user_skills: list, company: str, role: str, job_description: str = "", resume_text: str = "") -> str:
    """
    Generates a tailored 3-paragraph professional cover letter based on role, company, and extracted skills.
    """
    skills_text = ", ".join(user_skills) if user_skills else "software engineering, problem solving, and Python"
    comp_name = company.strip() if company.strip() else "your esteemed company"
    role_name = role.strip() if role.strip() else "Software Developer"

    client = get_groq_client()
    if client:
        prompt = f"""
Write a professional, compelling, and tailored 3-paragraph cover letter for:
Candidate applying for: {role_name}
Target Company: {comp_name}
Candidate Key Skills: {skills_text}
Optional Job Description: {job_description[:1000] if job_description else 'N/A'}
Additional Resume Context: {resume_text[:1000] if resume_text else 'N/A'}

Guidelines:
- Tone: Confident, respectful, and articulate.
- Paragraph 1: Enthusiastic introduction expressing excitement for {role_name} at {comp_name}.
- Paragraph 2: Core technical strengths mentioning skills ({skills_text}) and how they solve company problems.
- Paragraph 3: Professional closing with call to action requesting an interview.
- Add standard placeholders [Your Name], [Your Phone], [Your Email], [LinkedIn Profile] at the bottom.
"""
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an elite career strategist and executive cover letter author."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1200
                )
                return completion.choices[0].message.content
            except Exception:
                continue

    # Fallback template
    return f"""Dear Hiring Team at {comp_name},

I am writing to express my enthusiastic interest in the {role_name} position at {comp_name}. With a strong foundation in {skills_text} and a passion for building scalable software, I am eager to contribute effectively to your engineering goals and dynamic team culture.

Throughout my academic coursework and project experience, I have developed solid problem-solving abilities and practical expertise in modern software development. My hands-on work with {skills_text} has equipped me to write clean, maintainable code, troubleshoot issues efficiently, and collaborate seamlessly across teams. I am confident that my technical skills and quick learning ability make me a strong candidate for {comp_name}.

I would welcome the opportunity to discuss how my qualifications, dedication, and energy align with your current openings. Thank you for your time and consideration.

Sincerely,

[Your Name]
[Your Email] | [Your Phone Number]
[LinkedIn Profile / GitHub Profile]"""

def generate_followup_email(email_type: str, company: str, role: str, interviewer_name: str = "", notes: str = "") -> str:
    """
    Generates a follow-up email template based on type:
    - Post-Interview Thank You
    - Application Status Follow-up
    - Offer / Decision Follow-up
    """
    comp = company.strip() if company.strip() else "[Company Name]"
    pos = role.strip() if role.strip() else "[Job Role]"
    interviewer = interviewer_name.strip() if interviewer_name.strip() else "Hiring Manager"

    client = get_groq_client()
    if client:
        prompt = f"""
Write a professional follow-up email.
Email Type: {email_type}
Company: {comp}
Role: {pos}
Interviewer Name: {interviewer}
Specific Notes or Highlights: {notes if notes else 'Express appreciation and reiterate fit'}

Provide:
1. A clear Subject line
2. A polished, warm, and professional email body.
"""
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert corporate communications coach. Format with clear Subject and Body."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                return completion.choices[0].message.content
            except Exception:
                continue

    # Fallbacks based on email_type
    if "interview" in email_type.lower():
        return f"""Subject: Thank you for the interview — {pos} — [Your Name]

Dear {interviewer},

Thank you very much for taking the time to speak with me today regarding the {pos} position at {comp}. I truly enjoyed learning more about the team's objectives and upcoming projects.

Our conversation reinforced my enthusiasm for joining {comp}. I am excited about the opportunity to leverage my problem-solving skills and technical background to support your initiatives. {f'I especially enjoyed discussing {notes}.' if notes else ''}

Please let me know if you need any additional samples of my work or information. I look forward to hearing about the next steps.

Best regards,

[Your Name]
[Your Phone Number] | [Your Email]
[LinkedIn Profile]"""
    elif "offer" in email_type.lower():
        return f"""Subject: Checking in regarding {pos} application — [Your Name]

Dear {interviewer},

I hope this email finds you well.

I am writing to respectfully follow up on the status of my application for the {pos} role at {comp}. Following our previous discussions, I remain very enthusiastic about the opportunity to contribute to your team.

Could you kindly share any updates on the hiring timeline or if there is any further information I can provide?

Thank you again for your time and guidance.

Sincerely,

[Your Name]
[Your Contact Information]"""
    else:
        return f"""Subject: Follow-up on Job Application: {pos} — [Your Name]

Dear {interviewer},

I hope you are having a productive week.

I recently submitted my application for the {pos} position at {comp} and wanted to briefly reiterate my strong interest in this opportunity. 

With my technical skills and enthusiasm for {comp}'s mission, I believe I would be a great addition to the team. I have attached my resume for your convenience.

Thank you for your consideration, and I look forward to the possibility of discussing how I can add value to your team.

Warm regards,

[Your Name]
[Your Email] | [Your Phone Number]"""

def get_ai_response(messages: list, model: str = PRIMARY_MODEL) -> str:
    """
    Sends chat messages to Groq API with automatic fallback to secondary model.
    Falls back gracefully if network is unavailable or API key is unset.
    """
    client = get_groq_client()
    if client:
        for m in [model, FALLBACK_MODEL]:
            try:
                completion = client.chat.completions.create(
                    model=m,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                return completion.choices[0].message.content
            except Exception:
                continue

    # Offline / Fallback response if API cannot be reached
    user_query = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_query = msg.get("content", "").lower()
            break

    if "salary" in user_query or "negotiat" in user_query:
        return (
            "### 💰 Salary Negotiation Best Practices\n\n"
            "1. **Research Market Rates:** Use platforms like Levels.fyi, Glassdoor, and Payscale to establish a realistic target range.\n"
            "2. **Anchor with a Range:** Give a tight range with your target number at the bottom end.\n"
            "3. **Look Beyond Base Salary:** If base pay is fixed, negotiate sign-on bonuses, equity/RSUs, remote work flexibility, or additional PTO.\n"
            "4. **Express Enthusiasm:** Always frame your counter-offer positively: *'I am really excited about this role and confident in the impact I will make. Based on my experience and market data, I was hoping for...'*.\n\n"
            "*💡 Tip: Configure your live Groq API key in `.env` to get personalized AI responses.*"
        )
    elif "interview" in user_query or "question" in user_query:
        return (
            "### 🎯 Master the Behavioral Interview (STAR Method)\n\n"
            "- **Situation:** Briefly describe the background, challenge, or context (15-20% of your time).\n"
            "- **Task:** Explain what you were specifically responsible for achieving.\n"
            "- **Action:** Walk through the specific steps **you** took. Use strong active verbs ('architected', 'led', 'implemented').\n"
            "- **Result:** Quantify the business outcome (e.g., 'reduced latency by 35%', 'saved 10 engineering hours/week').\n\n"
            "#### Questions to Ask Your Interviewer:\n"
            "1. *What does success look like in this role in the first 90 days?*\n"
            "2. *What is the biggest engineering or product challenge the team is solving right now?*\n\n"
            "*💡 Tip: Configure your live Groq API key in `.env` to practice custom mock interview questions.*"
        )
    else:
        return (
            "### 🚀 Career Advisor Insights\n\n"
            "Here are recommended actions for your career development:\n"
            "- **Focus on Measurable Outcomes:** Ensure your resume and stories highlight metrics and measurable business value.\n"
            "- **Target Networking:** Reach out to 3-5 hiring managers or alumni in your desired roles weekly.\n"
            "- **Continuous Upskilling:** Build tangible portfolio projects demonstrating current industry tools.\n\n"
            "*💡 Note: Connect your live Groq API key in `.env` for deep real-time LLM-driven career guidance.*"
        )
