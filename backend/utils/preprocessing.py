import cv2
import numpy as np
from pdf2image import convert_from_path

POPPLER_PATH = r"E:\Users\fazal\Release-25.12.0-0\poppler-25.12.0\Library\bin"  # change if needed

def load_image(file_path):
    try:
        if file_path.lower().endswith(".pdf"):
            pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
            pil_image = pages[0]   # first page
            image = np.array(pil_image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        else:
            image = cv2.imread(file_path)
            return image
    except Exception as e:
        print("Error loading image:", e)
        return None


def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise(gray_image):
    return cv2.GaussianBlur(gray_image, (5, 5), 0)


def contrast_enhancement(denoised_image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(denoised_image)


def threshold(enhanced_image):
    return cv2.adaptiveThreshold(
        enhanced_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )


def preprocess(image):
    gray = convert_to_grayscale(image)
    denoised = denoise(gray)
    enhanced = contrast_enhancement(denoised)
    binary = threshold(enhanced)
    return binary


def save_image(image, path):
    cv2.imwrite(path, image)
