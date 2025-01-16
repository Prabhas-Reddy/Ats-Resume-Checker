import streamlit as st
import docx
import fitz  # PyMuPDF for PDF extraction
from io import StringIO
from collections import Counter

# Predefined list of roles and skills
# Expanded list of roles and skills
role_skills = {
    "Software Engineer": ["python", "java", "c++", "data structures", "algorithms", "software development", "object-oriented programming"],
    "Data Scientist": ["python", "machine learning", "data analysis", "statistics", "pandas", "numpy", "data visualization"],
    "Web Developer": ["html", "css", "javascript", "react", "angular", "web development", "node.js", "frontend", "backend"],
    "Product Manager": ["product management", "business strategy", "project management", "agile", "scrum", "leadership"],
    "UI/UX Designer": ["design", "user interface", "user experience", "wireframing", "figma", "adobe XD", "prototyping"],
    "DevOps Engineer": ["ci/cd", "docker", "kubernetes", "linux", "aws", "azure", "terraform", "infrastructure", "monitoring"],
    "Cybersecurity Analyst": ["security", "vulnerability assessment", "penetration testing", "network security", "firewalls", "incident response"],
    "Digital Marketer": ["seo", "sem", "google analytics", "content marketing", "social media", "email marketing", "ppc"],
    "HR Manager": ["recruitment", "talent management", "employee engagement", "performance management", "training", "onboarding"],
    "Finance Analyst": ["financial modeling", "budgeting", "forecasting", "excel", "accounting", "investment analysis", "risk management"],
    "Medical Professional": ["clinical care", "diagnosis", "treatment", "patient management", "medical terminology", "healthcare"],
    "Mechanical Engineer": ["cad", "solidworks", "autocad", "mechanical design", "manufacturing", "thermodynamics", "engineering analysis"],
    "Electrical Engineer": ["circuit design", "power systems", "electrical testing", "pcb design", "automation", "matlab", "embedded systems"],
    "Content Writer": ["copywriting", "creative writing", "seo", "blogging", "editing", "proofreading", "content strategy"],
    "Customer Service Representative": ["customer support", "problem-solving", "communication", "crm tools", "conflict resolution"],
    "Sales Manager": ["sales strategy", "lead generation", "crm", "negotiation", "market research", "business development"],
    "Graphic Designer": ["adobe photoshop", "adobe illustrator", "graphic design", "branding", "typography", "visual storytelling"],
    "Game Developer": ["unity", "unreal engine", "game design", "c#", "game physics", "animation", "ai in games"],
    "AI/ML Engineer": ["tensorflow", "keras", "deep learning", "nlp", "computer vision", "scikit-learn", "pytorch", "data modeling"],
    "Civil Engineer": ["structural design", "construction management", "autocad", "surveying", "building codes", "project planning"],
    "Data Engineer": ["big data", "hadoop", "spark", "sql", "etl", "data pipelines", "data lakes"],
    "Economist": ["economic modeling", "forecasting", "data analysis", "macroeconomics", "policy analysis", "statistics"],
    "Event Planner": ["event management", "budgeting", "vendor coordination", "public relations", "venue selection", "logistics"],
    "Legal Advisor": ["legal research", "contracts", "litigation", "compliance", "corporate law", "intellectual property"],
    "Teacher": ["curriculum planning", "classroom management", "student engagement", "lesson planning", "assessment"],
    "Environmental Scientist": ["ecology", "environmental impact", "sustainability", "data collection", "research", "policy analysis"],
}

# Function to extract text from DOCX files
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Open from in-memory byte stream
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# Function to calculate the ATS score (simple keyword matching)
def calculate_ats_score(resume_text, job_description=None):
    if job_description:  # If job description is provided
        resume_words = set(resume_text.lower().split())
        job_desc_words = set(job_description.lower().split())
        common_words = resume_words.intersection(job_desc_words)
        missing_keywords = job_desc_words - resume_words
        ats_score = len(common_words) / len(job_desc_words) * 100
        return round(ats_score, 2), common_words, missing_keywords
    else:
        # If no job description is provided, calculate a default score based on resume content
        return round((len(resume_text.split()) / 1000) * 100, 2), [], []

# Function to get keyword highlights
def highlight_keywords(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    job_desc_words = set(job_description.lower().split())
    common_words = resume_words.intersection(job_desc_words)
    
    highlighted_text = resume_text
    for word in common_words:
        highlighted_text = highlighted_text.replace(word, f"<mark>{word}</mark>")
    return highlighted_text

# Function to suggest roles based on resume skills
def suggest_roles(resume_text):
    # Convert resume text to lowercase and split it into words
    resume_words = set(resume_text.lower().split())
    
    # Find roles based on skills
    matched_roles = []
    for role, skills in role_skills.items():
        common_skills = resume_words.intersection(set(map(str.lower, skills)))
        if common_skills:
            matched_roles.append((role, list(common_skills)))
    
    return matched_roles

# Function to give feedback based on low ATS score
def give_feedback(ats_score, missing_keywords):
    if ats_score < 50:  # If the ATS score is less than 50%
        feedback = "Your resume could be optimized to match the job description more closely. Here are some suggestions:"
        feedback += f"\n\n- Add the following keywords or skills that are missing from your resume:\n"
        if missing_keywords:
            for word in missing_keywords:
                feedback += f"  - {word}\n"
        else:
            feedback += "  - No missing keywords were found, but consider tailoring your experience to the role.\n"
        feedback += "\n- Ensure your experience and skills are well-aligned with the role.\n"
        feedback += "- Try to highlight relevant experiences more clearly in your resume."
        return feedback
    return "Your resume is well-aligned with the job description."

# Mock ChatGPT API for ATS score (simulated function)
def chatgpt_ats_score(resume_text, job_description):
    # Normally, here you'd call the OpenAI API to analyze the resume and job description
    return calculate_ats_score(resume_text, job_description)

# Streamlit app layout
st.title("ATS Resume Checker")
st.markdown("Upload your resume and job description to calculate the ATS score.")

# File uploader for resume
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

# Input fields for job description and role (optional)
job_description = st.text_area("Job Description (Optional)")
role = st.text_input("Role (Optional)")

# Initialize variables
resume_text = ""

# ATS Score calculation when file is uploaded and generate button clicked
if resume_file is not None:
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(resume_file)
    elif resume_file.type == "text/plain":
        resume_text = StringIO(resume_file.getvalue().decode("utf-8")).read()

    st.subheader("Resume Text Preview:")
    st.write(resume_text[:1000])  # Display first 1000 characters for preview

# Resume Length Analysis
if resume_text:
    word_count = len(resume_text.split())
    st.write(f"Word Count: {word_count} words.")
    if word_count < 500:
        st.warning("Your resume might be too short. Consider adding more details.")
    elif word_count > 1000:
        st.warning("Your resume might be too long. Try to shorten it.")

# Generate ATS Score button
if st.button("Generate ATS Score"):
    if resume_text:
        ats_score, common_keywords, missing_keywords = chatgpt_ats_score(resume_text, job_description)
        st.subheader(f"ATS Score: {ats_score}%")
        
        if job_description:
            # Highlight matching keywords in the resume text
            highlighted_resume = highlight_keywords(resume_text, job_description)
            st.markdown("**Highlighted Keywords**:")
            st.markdown(highlighted_resume, unsafe_allow_html=True)
        
        # Display feedback if ATS score is low
        feedback = give_feedback(ats_score, missing_keywords)
        st.markdown(feedback)
        
        # Suggest roles based on skills found in the resume
        suggested_roles = suggest_roles(resume_text)
        if suggested_roles:
            st.subheader("Suggested Roles Based on Resume Skills:")
            for role, skills in suggested_roles:
                st.write(f"- **{role}**: Skills match: {', '.join(skills)}")
        else:
            st.write("No relevant roles found based on the skills in your resume.")
    else:
        st.warning("Please upload a resume to get the ATS score.")
