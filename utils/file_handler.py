import os
import zipfile
import fitz  # PyMuPDF
import docx
from utils.text_cleaner import clean_text

def extract_zip_and_read_texts(zip_path, extract_to):
    texts = []
    
    # Extract ZIP contents to the specified directory
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Walk through all folders and subfolders
    for root, _, files in os.walk(extract_to):
        for file in files:
            path = os.path.join(root, file)
            if file.lower().endswith('.pdf'):
                try:
                    texts.append(clean_text(read_pdf(path)))
                except Exception as e:
                    print(f"❌ Error reading PDF: {file} — {e}")
            elif file.lower().endswith('.docx'):
                try:
                    texts.append(clean_text(read_docx(path)))
                except Exception as e:
                    print(f"❌ Error reading DOCX: {file} — {e}")
            elif file.lower().endswith('.txt'):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        texts.append(clean_text(f.read()))
                except Exception as e:
                    print(f"❌ Error reading TXT: {file} — {e}")

    return texts

def read_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])
