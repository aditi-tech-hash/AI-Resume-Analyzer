import streamlit as st
import os
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and get an instant ATS-style analysis.")
st.markdown("### upload your resume and get an instant analysis")
st.write("This tool analyzes your resume, calculates a score, identifies missing skills, and provides improvement suggestions.")


uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

if uploaded_file:
    st.success("Resume Uploaded Successfully!")

    file_details = {
        "Filename": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size (KB)": round(uploaded_file.size / 1024, 2)
    }

    st.write("Resume Details:")
    st.write(file_details)
    st.write("Reached here")
    st.write("File Type:", uploaded_file.type)
    content = uploaded_file.read().decode("utf-8")
    st.write("Content Length:", len(content))
    st.write(content)
    if uploaded_file.type == "text/plain":
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        pdf = PdfReader (uploaded_file)
        content = " "

        for page in pdf.pages:
            content += page.extract_text()

    st.subheader("Resume content")
    st.write(content)
    score = 0

    keywords = [
            "python",
            "java",
            "sql",
            "html",
            "css",
            "javascript",
            "projects",
            "skill",
            "communication",
            "teamwork"
        ]

    for word in keywords:
            if word.lower() in content.lower():
                score += 20
    if score > 100:
          score = 100

    st.subheader("Resume Score")
    st.progress(score / 100)
    st.write(f"score: {score}/100")
    fig, ax = plt.subplots()
    ax.pie([score, 100-score],
           labels=["Score", "Remaining"],
           autopct="%1.1f%%")

    st.pyplot(fig)

    if score >= 80:
            st.success("Excellent Score!")
    elif score >= 60:
            st.warning("Good Score!")
    else:
            st.error("Needs Improvement!")
    missing_skills = []
    st.write(missing_skills)

    for word in keywords:
            st.write("Missing:", missing_skills)
            if word.lower() not in content.lower():
                missing_skills.append(word)
    st.write("Skills Matched:", len(keywords) - len(missing_skills))
    st.write("Skills Missing:", len(missing_skills))

    st.subheader("Missing Skills")

    if missing_skills:
            for skill in missing_skills:
                st.error(skill)
            
    else:
            st.success("Great! No missing skills found.")
            
    st.subheader("Suggestions")
    report = f"""
Resume Score: {score}/100

Missing Skills:
{', '.join(missing_skills)}

Suggestion:
Excellent Resume!
"""
    report = f"""
Resume Score: {score}/100

Missing Skills:
{', '.join(missing_skills)}

Suggestions:
Resume Analysis Complete
"""

st.download_button(
    label="📥 Download Report",
    data=report,
    file_name="resume_report.txt",
    mime="text/plain"
)

if score < 60:
            st.warning("Add more technical skills and projects to improve your resume.")
elif score < 80:
            st.info("Good resume! Add certifications and more projects.")
else:
            st.success("Excellent Resume!")
    