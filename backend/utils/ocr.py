import pytesseract
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"

# ==========================================
# OCR EXTRACTION
# ==========================================
def extract_text(image):
    """
    Extract raw text from image using Tesseract OCR
    """
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        print("OCR Error:", e)
        return ""


# ==========================================
# CLEAN TEXT
# ==========================================
def clean_text(text):
    """
    Remove unwanted symbols and normalize spacing
    """
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


# ==========================================
# EXTRACT AADHAAR NUMBER
# ==========================================
def extract_aadhaar_number(text):
    """
    Aadhaar format: 12 digits (XXXX XXXX XXXX)
    """
    pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


# ==========================================
# EXTRACT DOB
# ==========================================
def extract_dob(text):
    """
    Extract Date of Birth formats:
    DD/MM/YYYY
    DD-MM-YYYY
    YYYY
    """
    patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None


# ==========================================
# CHECK IF KEYWORDS EXIST
# ==========================================
def contains_keywords(text):
    """
    Check Aadhaar specific keywords
    """
    keywords = [
        "Government of India",
        "Unique Identification Authority of India",
        "UIDAI",
        "Aadhaar"
    ]

    found = []
    for word in keywords:
        if word.lower() in text.lower():
            found.append(word)

    return found
