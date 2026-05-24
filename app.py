import streamlit as st
import pandas as pd
from pypdf import PdfReader
from groq import Groq

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI insights.")

# =========================
# GROQ CLIENT
# =========================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

# =========================
# PDF PROCESSING
# =========================

if uploaded_file:

    # Read PDF
    reader = PdfReader(uploaded_file)

    # Extract Text
    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # =========================
    # AI PROMPT
    # =========================

    prompt = f"""
    Analyze this resume professionally.

    Give the response STRICTLY in this format:

    Summary: ...
    Strengths: ...
    Weaknesses: ...
    Suggestions: ...
    Missing Skills: ...
    Rating: ...

    Resume:
    {text}
    """

    # =========================
    # AI RESPONSE
    # =========================

    with st.spinner("Analyzing Resume..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    analysis = response.choices[0].message.content

    # =========================
    # PARSE AI RESPONSE
    # =========================

    sections = {
        "Summary": "",
        "Strengths": "",
        "Weaknesses": "",
        "Suggestions": "",
        "Missing Skills": "",
        "Rating": ""
    }

    lines = analysis.split("\n")

    for line in lines:

        if ":" in line:

            key, value = line.split(":", 1)

            key = key.strip()

            value = value.strip()

            if key in sections:
                sections[key] = value

    # =========================
    # CREATE TABLE
    # =========================

    df = pd.DataFrame({
        "Category": sections.keys(),
        "Analysis": sections.values()
    })

    # =========================
    # DISPLAY TABLE
    # =========================

    st.subheader("📊 Resume Analysis")

    st.table(df)
