import streamlit as st
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

    text = ""

    # Extract Text
    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # =========================
    # PROMPT
    # =========================

    prompt = f"""
    Analyze this resume professionally.

    Give:
    - Professional Summary
    - Key Strengths
    - Weaknesses
    - Suggestions For Improvement
    - Missing Technical Skills
    - Overall Resume Rating out of 10

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
    # DISPLAY RESULTS
    # =========================

    st.subheader("📊 Resume Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.info("📝 Professional Summary")
        st.write(analysis)

    with col2:

        st.success("✅ AI Analysis Completed")

        st.metric(
            label="Resume Status",
            value="Analyzed"
        )

        st.metric(
            label="AI Model",
            value="Llama 3.1"
        )
