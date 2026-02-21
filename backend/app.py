import os
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

# CNN
from models.cnn_predict import predict_image

# Preprocessing
from utils.preprocessing import (
    load_image,
    preprocess_for_cnn,
    preprocess_for_ocr
)

# OCR
from utils.ocr import (
    extract_text,
    clean_text,
    extract_aadhaar_number,
    extract_dob,
    contains_keywords
)

# ===============================
# FLASK CONFIG
# ===============================

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===============================
# MAIN ROUTE
# ===============================

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "Empty filename"}), 400

    # Save file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Load image (handles pdf + image)
    image = load_image(filepath)

    if image is None:
        return jsonify({"status": "error", "message": "Invalid image"}), 400

    # ===============================
    # 1️⃣ CNN PREPROCESS
    # ===============================
    cnn_input = preprocess_for_cnn(image)

    # ===============================
    # 2️⃣ CNN PREDICTION
    # ===============================
    score, decision = predict_image(cnn_input)

    # ===============================
    # 3️⃣ OCR PREPROCESS
    # ===============================
    ocr_ready = preprocess_for_ocr(image)

    # ===============================
    # 4️⃣ OCR EXTRACTION
    # ===============================
    raw_text = extract_text(ocr_ready)
    cleaned_text = clean_text(raw_text)

    aadhaar_number = extract_aadhaar_number(cleaned_text)
    dob = extract_dob(cleaned_text)
    keywords_found = contains_keywords(cleaned_text)

    # ===============================
    # FINAL RESPONSE
    # ===============================
    response = {
        "status": "success",
        "cnn_score": round(float(score), 4),
        "cnn_decision": decision,
        "aadhaar_number": aadhaar_number,
        "dob": dob,
        "keywords_found": keywords_found,
        "extracted_text": cleaned_text
    }

    return jsonify(response)


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)