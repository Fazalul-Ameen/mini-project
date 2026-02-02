from utils.text_utils import *

def day1_validation(raw_text):
    cleaned = clean_text(raw_text)

    aadhaars = extract_aadhaar_number(cleaned)
    keywords = keyword_check(cleaned)
    dob = extract_dob(cleaned)

    result = {
        "aadhaar_found": bool(aadhaars),
        "aadhaar_valid": False,
        "keywords_found": keywords,
        "dob_valid": False
    }

    if aadhaars:
        result["aadhaar_valid"] = validate_aadhaar_number(aadhaars[0])

    if dob:
        result["dob_valid"] = validate_dob(dob)

    return result
