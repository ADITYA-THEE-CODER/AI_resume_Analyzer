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

    # Store Extracted Text
    text = ""

    # Extract Text From Pages
    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # =========================
    # CREATE PROMPT
    # =========================

    prompt = f"""
    Analyze this resume professionally.

    Give:
    1. Short Professional Summary
    2. Key Strengths
    3. Weaknesses
    4. Suggestions For Improvement
    5. Missing Technical Skills
    6. Overall Resume Rating out of 10

    Keep the response concise and structured.

    Resume:
    {text}
    """

    # =========================
    # SEND TO GROQ
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

    # =========================
    # EXTRACT RESPONSE
    # =========================

    analysis = response.choices[0].message.content

    # =========================
    # DISPLAY RAW ANALYSIS
    # =========================

    st.subheader("📌 Resume Analysis")

    st.write(analysis)

    # =========================
    # CREATE TABLE DATA
    # =========================

    data = {
        "Category": [
            "Professional Summary",
            "Key Strengths",
            "Weaknesses",
            "Suggestions",
            "Missing Skills",
            "Resume Rating"
        ],

        "Status": [
            "Generated",
            "Analyzed",
            "Analyzed",
            "Generated",
            "Detected",
            "Calculated"
        ]
    }

    # =========================
    # CREATE DATAFRAME
    # =========================

    df = pd.DataFrame(data)

    # =========================
    # DISPLAY TABLE
    # =========================

    st.subheader("📊 Analysis Overview")

    st.dataframe(
        df,
        use_container_width=True
    )
