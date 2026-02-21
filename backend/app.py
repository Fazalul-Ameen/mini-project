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
    print("CNN Decision:", decision)

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
    # FINAL RESPONSE (MATCH FRONTEND)
    # ===============================

    final_decision = decision  # You can improve this logic later

    response = {
        "status": "success",
        "cnn_prediction": decision,
        "cnn_confidence": round(float(score), 4),
        "rule_score": 1 if keywords_found else 0,
        "rule_decision": "Valid Keywords" if keywords_found else "Missing Keywords",
        "final_decision": final_decision,
        "aadhaar_number": aadhaar_number,
        "dob": dob
    }

    return jsonify(response)


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)