import pytesseract
import cv2

#tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"  # change if needed

def extract_text(image):
    text = pytesseract.image_to_string(
        image,
        config="--oem 3 --psm 6"
    )
    return text
  