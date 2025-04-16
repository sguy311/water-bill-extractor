import cv2
import numpy as np

def preprocess_image(image):
    """Preprocess image to improve OCR results."""
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply slight Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    threshold = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Invert the image (black text on white background)
    inverted = cv2.bitwise_not(threshold)
    
    # Optional: perform additional preprocessing as needed
    # - Deskew the image if text is not horizontal
    # - Remove borders
    # - Enhance contrast
    
    return inverted