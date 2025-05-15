import streamlit as st
import os
import zipfile
import tempfile
from utils.file_handler import extract_zip_and_read_texts
from utils.summarizer import summarize_texts

st.title("📄 AI Proposal Generator")
st.write("Upload a ZIP file with PDF, DOCX, or TXT files. The AI will extract and summarize them into a draft proposal.")

uploaded_zip = st.file_uploader("Upload ZIP file", type=["zip"])

if uploaded_zip:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        texts = extract_zip_and_read_texts(zip_path, temp_dir)

        if texts:
            summary = summarize_texts(texts)
            st.subheader("📑 Generated Proposal Draft")
            st.text_area("Output", summary, height=300)
            st.download_button("Download Proposal", summary, file_name="proposal.txt")
        else:
            st.warning("No valid files found in the ZIP.")
