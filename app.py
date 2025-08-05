import streamlit as st
import PyPDF2
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in text.split() if word.isalpha()]
    words = [w for w in words if w not in stop_words]
    return set(words)

def suggest_learning(skills):
    base_url = "https://www.coursera.org/search?query="
    return {skill: base_url + skill for skill in skills}

st.title("📄 Resume Skill Analyzer")
st.write("Upload your resume and paste the job description to see skill matches.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if resume_file and job_description:
    resume_text = extract_text_from_pdf(resume_file)
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills
    match_score = round(len(matched_skills) / len(job_skills) * 100, 2)

    st.subheader("Results")
    st.write(f"**Match Score:** {match_score}%")
    st.write("✅ **Matched Skills:**", ", ".join(matched_skills))
    st.write("❌ **Missing Skills:**", ", ".join(missing_skills))

    if missing_skills:
        st.subheader("📚 Learn Missing Skills")
        links = suggest_learning(missing_skills)
        for skill, url in links.items():
            st.markdown(f"- [{skill}]({url})")

