from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})

    file = request.files['document']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({
        "status": "success",
        "message": "File uploaded successfully",
        "filename": file.filename
    })

if __name__ == '__main__':
    app.run(debug=True)
