import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI insights.")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.write(text)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
