import os
import email
import ollama
import hashlib
import csv
import fitz  # PyMuPDF for PDF extraction
import docx
import pytesseract
from PIL import Image
from email import policy
from email.parser import BytesParser
from rapidfuzz import fuzz
import re
import csv
import importlib

# Extract text from email body
def extract_text_from_email(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            text = msg.get_body(preferencelist=('plain')).get_content()
    except Exception as e:
        print(f"Error reading email {file_path}: {e}")
    return text.strip()

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text.strip()

# Extract text from a Word document (DOCX)
def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
    return text.strip()

# Extract text from an image using OCR
def extract_text_from_image(image_path):
    text = ""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
    return text.strip()

# Process attachments and extract text
def extract_text_from_attachments(msg):
    extracted_text = ""
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename:
            content_type = part.get_content_type()
            data = part.get_payload(decode=True)
            temp_path = f"./temp_{filename}"
            with open(temp_path, "wb") as temp_file:
                temp_file.write(data)

            # Determine file type and extract text accordingly
            if content_type == "application/pdf":
                extracted_text += extract_text_from_pdf(temp_path) + "\n"
            elif content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                extracted_text += extract_text_from_docx(temp_path) + "\n"
            elif content_type.startswith("image/"):
                extracted_text += extract_text_from_image(temp_path) + "\n"

            os.remove(temp_path)
    
    return extracted_text.strip()

# Compute hash to detect duplicate emails
def is_duplicate(email_text, seen_emails):
    for existing_email in seen_emails:
        similarity = fuzz.ratio(email_text, existing_email)
        if similarity > 85:
            return True
    return False

# Process emails and classify them
def process_emails(folder_path, model):
    model_mapping = {
        "gpt-4o-mini": "classify_OpenAI",
        "llama3": "classify_llama3",
        "gemini": "GeminiClassifier"
    }

    module_name = model_mapping[model]
    module = importlib.import_module(module_name)
    classify_email = getattr(module, "classify_email")

    seen_emails = []
    results = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith(".txt") or file_name.endswith(".eml"):
            with open(file_path, "rb") as f:
                msg = BytesParser(policy=policy.default).parse(f)

            email_body_text = extract_text_from_email(file_path)
            attachment_text = extract_text_from_attachments(msg)
            combined_text = email_body_text + "\n" + attachment_text

            
            is_dup = is_duplicate(combined_text, seen_emails)
            print(f"\nProcessing Email: {file_name}\nDuplicate: {is_dup}")

            if is_dup:
                print(f"Skipping duplicate email: {file_name}")
                results.append({
                    "email": file_name,
                    "duplicate": True,
                    "classification": "Skipped",
                    "confidence": "N/A"
                })
                continue

            seen_emails.append(combined_text)
            classification = classify_email(combined_text)
            # Add email name and duplicate status to classification result
            classification["email"] = file_name
            classification["duplicate"] = False

            results.append(classification)
            print(f"Classification: {classification}")
    return results


# Run extraction, duplicate detection, and classification
#process_emails("C:/Users/Sakshi Srivastava/Desktop/hackathon/emails")
