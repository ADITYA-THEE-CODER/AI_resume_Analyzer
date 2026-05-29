import streamlit as st
from pypdf import PdfReader
from groq import Groq
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get structured AI insights.")

# =========================================
# GROQ CLIENT
# =========================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

# =========================================
# PDF PROCESSING
# =========================================

if uploaded_file:

    # Read PDF
    reader = PdfReader(uploaded_file)

    # Extract text
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # =========================================
    # AI PROMPT
    # =========================================

    prompt = f"""
    Analyze this resume and provide:

    1. Professional Summary
    2. Key Skills
    3. Strengths
    4. Weaknesses
    5. Suggested Job Roles
    6. ATS Score out of 100

    Resume:
    {text}

    Keep the response professional and concise.
    """

    # =========================================
    # SEND TO GROQ
    # =========================================

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # =========================================
    # EXTRACT RESPONSE
    # =========================================

    result = response.choices[0].message.content

    # =========================================
    # DISPLAY RAW AI OUTPUT
    # =========================================

    st.subheader("📄 AI Resume Analysis")

    st.write(result)

    # =========================================
    # SIMPLE FEATURE TABLE
    # =========================================

    data = {
        "Feature": [
            "Resume Uploaded",
            "Characters Extracted",
            "AI Model Used"
        ],

        "Value": [
            "Yes",
            len(text),
            "llama-3.1-8b-instant"
        ]
    }

    df = pd.DataFrame(data)

    st.subheader("📊 Resume Analysis Overview")

    st.table(df)
