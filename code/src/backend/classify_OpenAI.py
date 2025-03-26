# Classify email content

from CsvFileReader import load_request_types
import re
from openai import OpenAI

csv_file = "C:/Users/Sakshi Srivastava/Desktop/hackathon/request_types_utf8.csv"
def classify_email(email_text):
    request_types = load_request_types(csv_file)
    prompt = f"""
    Classify the following email into a request type and sub-request type:
    
    Email & Attachment Content: {email_text}
    
    Possible Request Types:
    {', '.join(request_types.keys())}
    
    Sub-Request Types:
    {', '.join([f'{k}: {', '.join(v)}' for k, v in request_types.items()])}
    
    
    Analyze the following email and extract the relevant details dynamically.
    Email can contain multiple request types and sub-request type and also find any other important details like deal name, amount , expiration date and any relevant information.
    
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

     # Call Groq API with the selected model
    '''response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Choose your model from Groq
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512
    )'''

    client = OpenAI(
         api=""
    )

    response = client.chat.completions.create(
                 model="gpt-4o-mini",
                 store=True,
                 messages=[{"role": "user", "content": prompt}])

    # Extract response
    classification_result = response.choices[0].message.content
    print(classification_result)
    return extract_fields(classification_result)
    



import re
from collections import defaultdict

def extract_fields(response_text):
    extracted_data = {
        "Request Type": None,
        "Sub-Request Type": None,
        "Reason": None,
        "Confidence": None,
        "Extracted Fields": defaultdict(list)  # Use defaultdict to store multiple values per field
    }

    # Extract Request Type
    request_match = re.search(r"Request Type:\s*(.+)", response_text)
    if request_match:
        extracted_data["Request Type"] = request_match.group(1).strip()

    # Extract Sub-Request Type
    sub_request_match = re.search(r"Sub-Request Type:\s*(.+)", response_text)
    if sub_request_match:
        extracted_data["Sub-Request Type"] = sub_request_match.group(1).strip()

    # Extract Reason
    reason_match = re.search(r"Reason:\s*(.+)", response_text)
    if reason_match:
        extracted_data["Reason"] = reason_match.group(1).strip()

    # Extract Confidence
    confidence_match = re.search(r"Confidence:\s*(\d+)", response_text)
    if confidence_match:
        extracted_data["Confidence"] = int(confidence_match.group(1))

    # Convert single-value lists into plain strings
    extracted_fields_match = re.search(r"Extracted Fields:\s*(.*)", response_text, re.DOTALL)
    if extracted_fields_match:
        extracted_data["Extracted Fields"] = extracted_fields_match.group(1).strip()

    return extracted_data
