import streamlit as st
from PyPDF2 import PdfReader

import nltk
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --------------------------------
# Download NLTK Data
# --------------------------------

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# --------------------------------
# Extract PDF Text
# --------------------------------

def extract_pdf_text(file):

    text = ""

    reader = PdfReader(file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# --------------------------------
# Text Cleaning
# --------------------------------

stop_words = set(stopwords.words('english'))

def preprocess_text(text):

    # lowercase
    text = text.lower()

    # remove symbols
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # tokenize
    words = word_tokenize(text)

    # remove stopwords
    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(filtered_words)


# --------------------------------
# Skills List
# --------------------------------

skills = [
    "python",
    "sql",
    "machine learning",
    "flask",
    "java",
    "communication"
]


# --------------------------------
# Skill Matching Function
# --------------------------------

def calculate_skill_match(resume_text):

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in resume_text:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    score = (
        len(matched_skills) / len(skills)
    ) * 100

    return matched_skills, missing_skills, round(score, 2)


# --------------------------------
# STREAMLIT UI
# --------------------------------

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description"
)

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        # Extract Resume Text
        resume_text = extract_pdf_text(uploaded_file)

        # Clean Resume Text
        clean_resume = preprocess_text(resume_text)

        # Skill Matching
        matched_skills, missing_skills, score = calculate_skill_match(clean_resume)

        # Status
        if score >= 50:
            status = "Shortlisted"
        else:
            status = "Rejected"

        # --------------------------------
        # OUTPUT
        # --------------------------------

        st.success("Resume Analysis Completed!")

        st.subheader("Match Score")
        st.write(f"{score}%")

        st.subheader("Matched Skills")
        st.text(", ".join(matched_skills))

        st.subheader("Missing Skills")
        st.text(", ".join(missing_skills))

        st.subheader("Status")
        st.write(status)

    else:
        st.warning("Please upload resume and enter job description")