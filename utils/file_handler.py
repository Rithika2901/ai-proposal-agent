import os
import zipfile
import fitz  # PyMuPDF
import docx
from utils.text_cleaner import clean_text

def extract_zip_and_read_texts(zip_path, extract_to):
    texts = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    for root, _, files in os.walk(extract_to):
        for file in files:
            path = os.path.join(root, file)
            if file.lower().endswith('.pdf'):
                texts.append(clean_text(read_pdf(path)))
            elif file.lower().endswith('.docx'):
                texts.append(clean_text(read_docx(path)))
            elif file.lower().endswith('.txt'):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    texts.append(clean_text(f.read()))
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
