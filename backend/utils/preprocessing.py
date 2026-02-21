import cv2
import numpy as np
from pdf2image import convert_from_path

POPPLER_PATH = r"E:\Users\fazal\Release-25.12.0-0\poppler-25.12.0\Library\bin"


# ==========================
# LOAD IMAGE (PDF OR IMAGE)
# ==========================
def load_image(file_path):
    try:
        if file_path.lower().endswith(".pdf"):
            pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
            pil_image = pages[0]
            image = np.array(pil_image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        else:
            return cv2.imread(file_path)
    except Exception as e:
        print("Error loading image:", e)
        return None


# ==========================
# OCR PREPROCESSING
# ==========================
def preprocess_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    binary = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return binary


# ==========================
# CNN PREPROCESSING
# ==========================
def preprocess_for_cnn(image):
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    image = np.reshape(image, (1, 128, 128, 3))
    return image


# ==========================
# SAVE IMAGE
# ==========================
def save_image(image, path):
    cv2.imwrite(path, image)
