import os
import email
import ollama
import hashlib
import csv
from email import policy
from email.parser import BytesParser
import re
import csv
from CsvFileReader import load_request_types

csv_file = "C:/Users/Sakshi Srivastava/Desktop/hackathon/request_types_utf8.csv"
def classify_email(email_text):
    # Load request types dynamically from CSV
    request_types = load_request_types(csv_file)

# Print to verify (optional)
    print(request_types)
    prompt = f"""
    Classify the following email into a request type and sub-request type:
    
    Email & Attachment Content: {email_text}
    
    Possible Request Types:
    {', '.join(request_types.keys())}
    
    Sub-Request Types:
    {', '.join([f'{k}: {', '.join(v)}' for k, v in request_types.items()])}
    
    Analyze the following email and extract the relevant details dynamically.
    Email can contain multiple request types and sub-request type and also
    find any other important details like deal name, amount , expiration date and any relevant information.
    
    Response format:
    Request Type: <Type>
    Sub-Request Type: <Sub-Type>
    Reason: <Explanation>
    Confidence: <Score>
    Extracted Fields:
    - Field Name: <Value>
    - Field Name: <Value>
    - Field Name: <Value>
    
    Ensure:
    - "Request Type" and "Sub-Request Type" are always provided.
    -  Ensure the confidence score is always an **integer between 1-100**.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    classification_result = response["message"]["content"]
    print(classification_result)
    #dataafterparsing = parse_model_response(classification_result)
    return extract_fields(classification_result)
    
    #return classification_result, confidence_score

def extract_fields(classification_result):
    """
    Extracts request type, sub-request type, confidence score, reason, and extracted fields from model response.
    """

    extracted_data = {
        "request_type": "Unknown",
        "sub_request_type": "Unknown",
        "confidence_score": 0,
        "reason": "No reason provided.",
        "extracted_fields": "None"
    }

    # Extract Request Type, Sub-Request Type, Confidence, and Reason
    request_type_match = re.search(r"\*\*Request Type:\*\*\s*(.*?)\n", classification_result)
    sub_request_type_match = re.search(r"\*\*Sub-Request Type:\*\*\s*(.*?)\n", classification_result)
    confidence_match = re.search(r"\*\*Confidence:\*\*\s*(\d+)", classification_result)  # Fixed Regex
    reason_match = re.search(r"\*\*Reason:\*\*\s*(.*?)\n", classification_result)

    if request_type_match:
        extracted_data["request_type"] = request_type_match.group(1).strip()
    if sub_request_type_match:
        extracted_data["sub_request_type"] = sub_request_type_match.group(1).strip()
    if confidence_match:
        extracted_data["confidence_score"] = int(confidence_match.group(1).strip())
    if reason_match:
        extracted_data["reason"] = reason_match.group(1).strip()

    # Extract the entire "Extracted Fields" section
    extracted_fields_match = re.search(r"\*\*Extracted Fields:\*\*\n\n([\s\S]+?)(\n\n|$)", classification_result)

    if extracted_fields_match:
        extracted_data["extracted_fields"] = extracted_fields_match.group(1).strip()
    return extracted_data
