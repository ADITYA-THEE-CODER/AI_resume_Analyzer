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
st.write(summary)

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    prompt = f"""
    Summarize this resume professionally.

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = response.choices[0].message.content

    st.subheader("Resume Summary")

    st.write(summary)
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    prompt = f"""
    Summarize this resume professionally.

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = response.choices[0].message.content

    st.subheader("Resume Summary")

    st.write(summary)
prompt = f"""
Summarize this resume professionally.

Resume:
{text}
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

summary = response.choices[0].message.content

st.subheader("Resume Summary")

st.write(summary)
