import streamlit as st
from pypdf import PdfReader
from groq import Groq

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
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

    # Store extracted text
    text = ""

    # Extract text from every page
    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Create AI Prompt
    prompt = f"""
    Summarize this resume professionally.

    Resume:
    {text}
    """

    # Send to Groq LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract AI response
    summary = response.choices[0].message.content

    # Display summary
    st.subheader("Resume Summary")

    st.write(summary)
