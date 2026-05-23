import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI insights.")
