# trigger rebuild
import nltk
nltk.download('punkt')

import streamlit as st
import os
import zipfile
import tempfile
from utils.file_handler import extract_zip_and_read_texts, read_pdf, read_docx
from utils.text_cleaner import clean_text
from utils.summarizer import summarize_texts  # ✅ model is inside this function now

st.set_page_config(page_title="AI Proposal Generator", layout="centered")
st.title("📄 AI Proposal Generator")

st.write("Upload a **ZIP file** (multiple documents) or a single **PDF / DOCX / TXT** file. The AI will summarize and generate a professional draft.")

uploaded_file = st.file_uploader("Upload file", type=["zip", "pdf", "docx", "txt"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Detect file type and read
        if uploaded_file.name.endswith(".zip"):
            texts = extract_zip_and_read_texts(file_path, temp_dir)
        elif uploaded_file.name.endswith(".pdf"):
            texts = [clean_text(read_pdf(file_path))]
        elif uploaded_file.name.endswith(".docx"):
            texts = [clean_text(read_docx(file_path))]
        elif uploaded_file.name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                texts = [clean_text(f.read())]
        else:
            texts = []
            st.warning("Unsupported file type.")

        if texts and len(" ".join(texts)) > 100:
            with st.spinner("🧠 Generating summary..."):
                summary = summarize_texts(texts)
            st.subheader("📑 Generated Proposal")
            st.text_area("Summary Output", summary, height=300)
            st.download_button("Download Summary", summary, file_name="summary.txt")
        else:
            st.warning("No meaningful content found to summarize.")

