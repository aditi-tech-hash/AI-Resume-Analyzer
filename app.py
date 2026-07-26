import streamlit as st
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and get an instant ATS-style analysis.")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

if uploaded_file:

    content = ""

    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)

        for page in pdf.pages:
            text = page.extract_text()
            if text:
                content += text

    st.subheader("Resume Content")
    st.write(content)

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

    score = 0

    for word in keywords:
        if word.lower() in content.lower():
            score += 20

    if score > 100:
        score = 100

    st.subheader("Resume Score")
    st.progress(score / 100)
    st.write(f"Score: {score}/100")

    fig, ax = plt.subplots()
    ax.pie(
        [score, 100 - score],
        labels=["Score", "Remaining"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    missing_skills = []

    for word in keywords:
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

    if score >= 80:
        st.success("Excellent Resume!")
        suggestion = "Excellent Resume!"
    elif score >= 60:
        st.warning("Good Resume. Add more projects and certifications.")
        suggestion = "Add more projects and certifications."
    else:
        st.error("Resume needs improvement.")
        suggestion = "Add skills, projects and relevant keywords."

    report = f"""
Resume Score: {score}/100

Skills Matched: {len(keywords) - len(missing_skills)}
Skills Missing: {len(missing_skills)}

Missing Skills:
{', '.join(missing_skills)}

Suggestion:
{suggestion}
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )