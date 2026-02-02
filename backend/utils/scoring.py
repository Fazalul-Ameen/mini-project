def calculate_score(validation_result, raw_text):
    score = 0

    if validation_result["aadhaar_found"]:
        score += 30

    if validation_result["aadhaar_valid"]:
        score += 25

    if len(validation_result["keywords_found"]) >= 2:
        score += 20

    if validation_result["dob_valid"]:
        score += 15

    # basic OCR confidence: text length
    if len(raw_text.strip()) > 50:
        score += 10

    return score
