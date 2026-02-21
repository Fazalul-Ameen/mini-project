import re
from datetime import datetime

def normalize_ocr_text(text):
    replacements = {
        'O': '0',
        'I': '1',
        'L': '1',
        'S': '5',
        'B': '8'
    }

    corrected = ""
    for char in text:
        if char in replacements:
            corrected += replacements[char]
        else:
            corrected += char

    return corrected


def clean_text(text):
    text = text.upper()
    text = normalize_ocr_text(text) 
    text = re.sub(r'[^A-Z0-9:/ ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_aadhaar_number(text):
    patterns = [
        r'\b\d{4}\s?\d{4}\s?\d{4}\b',
        r'\b\d{12}\b'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text) 
        if matches:
            return matches

    return []


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
    # DD/MM/YYYY
    match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
    if match:
        return match.group()

    # YEAR OF BIRTH
    match = re.search(r'YEAR OF BIRTH[: ]*(\d{4})', text)
    if match:
        return match.group(1)

    # Just year
    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        return match.group()

    return None

def validate_dob(dob):
    year = int(dob.split("/")[-1])
    return year <= datetime.now().year
