import cv2
import numpy as np
from pdf2image import convert_from_path

def load_image(file_path):
    if file_path.lower().endswith(".pdf"):
        pages=convert_from_path(file_path)
        pil_image=pages[0]
        image=np.array(pil_image)
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        return image
    else:
        image=cv2.imread(file_path)
        return image
    
def convert_to_grayscale(image):   
    gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return gray_image

def denoise(gray_image):
    denoised_image=cv2.GaussianBlur(gray_image,(5,5),0)
    return denoised_image

def contrast_enhancement(denoised_image):
    clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    enhanced_image=clahe.apply(denoised_image)
    return enhanced_image

def threshold(enhanced_image):
    binary_image=cv2.adaptiveThreshold(enhanced_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return binary_image

def preprocess(image):
    gray=convert_to_grayscale(image)
    denoised=denoise(gray)
    enhanced=contrast_enhancement(denoised)
    binary=threshold(enhanced)
    return binary