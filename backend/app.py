from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.preprocessing import load_image, preprocess, save_image
from utils.ocr import extract_text
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})

    file = request.files['document']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Load image or PDF
    image = load_image(file_path)
    if image is None:
        return jsonify({"status": "error", "message": "Unsupported file"})

    # Preprocess
    processed_image = preprocess(image)

    # Save output
    processed_path = os.path.join(PROCESSED_FOLDER, "processed_" + file.filename + ".png")
    save_image(processed_image, processed_path)

    text = extract_text(processed_image)
    print(text)

    return jsonify({
        "status": "success",
        "message": "File uploaded and preprocessed",
        "processed_file": processed_path
    })

if __name__ == '__main__':
    app.run(debug=True)
