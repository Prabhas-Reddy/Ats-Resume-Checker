import streamlit as st
import docx
import fitz  # PyMuPDF for PDF extraction
from io import StringIO

# Predefined list of roles and skills
role_skills = {
    "Software Engineer": ["python", "java", "c++", "data structures", "algorithms", "software development", "object-oriented programming"],
    "Data Scientist": ["python", "machine learning", "data analysis", "statistics", "pandas", "numpy", "data visualization"],
    "Web Developer": ["html", "css", "javascript", "react", "angular", "web development", "node.js", "frontend", "backend"],
    "DevOps Engineer": ["ci/cd", "docker", "kubernetes", "linux", "aws", "azure", "terraform", "infrastructure", "monitoring"],
    "Cybersecurity Analyst": ["security", "vulnerability assessment", "penetration testing", "network security", "firewalls", "incident response"],
    "AI/ML Engineer": ["tensorflow", "keras", "deep learning", "nlp", "computer vision", "scikit-learn", "pytorch", "data modeling"],
    "Cloud Engineer": ["aws", "azure", "gcp", "cloud computing", "terraform", "kubernetes", "devops", "serverless"],
    "Backend Developer": ["node.js", "django", "flask", "spring boot", "sql", "mongodb", "rest api", "graphql"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue.js", "angular", "next.js", "redux"],
    "Embedded Systems Engineer": ["c", "c++", "embedded c", "microcontrollers", "rtos", "firmware development", "pcb design"],
    "Game Developer": ["unity", "unreal engine", "c#", "c++", "game design", "animation", "ai in games"],
    "Blockchain Developer": ["solidity", "ethereum", "smart contracts", "web3", "decentralized applications", "hyperledger"],
    "Full Stack Developer": ["javascript", "react", "node.js", "express", "mongodb", "graphql", "docker", "aws"],
    "Data Engineer": ["big data", "hadoop", "spark", "sql", "etl", "data pipelines", "data lakes"],
    "Product Manager": ["product management", "business strategy", "project management", "agile", "scrum", "leadership"],
    "UI/UX Designer": ["design", "user interface", "user experience", "wireframing", "figma", "adobe XD", "prototyping"],
    "Finance Analyst": ["financial modeling", "budgeting", "forecasting", "excel", "accounting", "investment analysis", "risk management"],
    "Electrical Engineer": ["circuit design", "power systems", "electrical testing", "pcb design", "automation", "matlab", "embedded systems"],
    "Mechanical Engineer": ["cad", "solidworks", "autocad", "mechanical design", "manufacturing", "thermodynamics", "engineering analysis"],
    "Civil Engineer": ["structural design", "construction management", "autocad", "surveying", "building codes", "project planning"],
    "Sales Manager": ["sales strategy", "lead generation", "crm", "negotiation", "market research", "business development"],
    "Content Writer": ["copywriting", "creative writing", "seo", "blogging", "editing", "proofreading", "content strategy"],
    "Graphic Designer": ["adobe photoshop", "adobe illustrator", "graphic design", "branding", "typography", "visual storytelling"],
    "Digital Marketer": ["seo", "sem", "google analytics", "content marketing", "social media", "email marketing", "ppc"],
    "Legal Advisor": ["legal research", "contracts", "litigation", "compliance", "corporate law", "intellectual property"],
    "HR Manager": ["recruitment", "talent management", "employee engagement", "performance management", "training", "onboarding"],
    "Teacher": ["curriculum planning", "classroom management", "student engagement", "lesson planning", "assessment"],
}


# Function to extract text from DOCX files
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return '\n'.join([para.text for para in doc.paragraphs])

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return '\n'.join([page.get_text() for page in doc])

# Function to calculate ATS score
def calculate_ats_score(resume_text, job_keywords):
    resume_words = set(resume_text.lower().split())
    job_desc_words = set(map(str.lower, job_keywords))
    common_words = resume_words.intersection(job_desc_words)
    missing_keywords = job_desc_words - resume_words
    ats_score = (len(common_words) / len(job_desc_words) * 100) if job_desc_words else 0
    return round(ats_score, 2), common_words, missing_keywords

# Streamlit app layout
st.title("ATS Resume Checker")
st.markdown("Upload your resume and enter a role or job description to calculate the ATS score.")

# File uploader for resume
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
job_description = st.text_area("Job Description (Optional)")
role = st.selectbox("Select Role (Optional)", [""] + list(role_skills.keys()))

resume_text = ""

if resume_file:
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(resume_file)
    elif resume_file.type == "text/plain":
        resume_text = StringIO(resume_file.getvalue().decode("utf-8")).read()

    st.subheader("Resume Preview:")
    st.write(resume_text[:1000])

# Generate ATS Score
if st.button("Generate ATS Score"):
    if resume_text:
        job_keywords = job_description.split() if job_description else []
        if role and role in role_skills:
            job_keywords.extend(role_skills[role])
        ats_score, common_keywords, missing_keywords = calculate_ats_score(resume_text, job_keywords)
        
        st.subheader(f"ATS Score: {ats_score}%")
        st.markdown("**Matched Keywords:** " + ", ".join(common_keywords))
        st.markdown("**Missing Keywords:** " + ", ".join(missing_keywords))
    else:
        st.warning("Please upload a resume first.")
