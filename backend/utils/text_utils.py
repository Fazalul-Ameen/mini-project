import re
from datetime import datetime

def clean_text(text):
    text = text.upper()
    text = re.sub(r'[^A-Z0-9:/ ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_aadhaar_number(text):
    return re.findall(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)

def validate_aadhaar_number(aadhaar):
    aadhaar = aadhaar.replace(" ", "")
    if len(aadhaar) != 12:
        return False
    if aadhaar[0] in ['0', '1']:
        return False
    return True

def keyword_check(text):
    keywords = [
        "GOVERNMENT OF INDIA",
        "AADHAAR",
        "UIDAI",
        "UNIQUE IDENTIFICATION"
    ]
    return [k for k in keywords if k in text]

def extract_dob(text):
    match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
    return match.group() if match else None

def validate_dob(dob):
    year = int(dob.split("/")[-1])
    return year <= datetime.now().year
