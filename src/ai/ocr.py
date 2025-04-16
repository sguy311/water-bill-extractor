import cv2
import pytesseract
import re
from datetime import datetime
from pathlib import Path

from models.bill_data import BillData
from ai.image_processor import preprocess_image

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Uncomment and adjust for Windows

def extract_bill_data(image_path):
    """Extract water bill data using OCR from an image file."""
    
    # Read and preprocess the image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to read image: {image_path}")
        return None
    
    processed_image = preprocess_image(image)
    
    # Perform OCR on the processed image
    text = pytesseract.image_to_string(processed_image)
    
    # Extract relevant information using regex patterns
    date_match = extract_date(text)
    usage_match = extract_usage(text)
    cost_match = extract_cost(text)
    
    if date_match and usage_match and cost_match:
        # Create and return BillData object
        return BillData(
            date=date_match,
            usage=usage_match,
            cost=cost_match
        )
    else:
        print("Failed to extract all required data from the bill")
        print(f"Date found: {date_match is not None}")
        print(f"Usage found: {usage_match is not None}")
        print(f"Cost found: {cost_match is not None}")
        return None

def extract_date(text):
    """Extract date from OCR text."""
    # Adjust regex patterns based on your specific bill format
    date_patterns = [
        r'(\d{1,2}/\d{1,2}/\d{2,4})',  # MM/DD/YYYY or M/D/YY
        r'(\d{1,2}-\d{1,2}-\d{2,4})',  # MM-DD-YYYY or M-D-YY
        r'([A-Z][a-z]+ \d{1,2},? \d{4})'  # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            try:
                # Try different date formats
                for fmt in ['%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y', '%B %d, %Y', '%B %d %Y']:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
            except Exception as e:
                print(f"Error parsing date: {e}")
    
    return None

def extract_usage(text):
    """Extract water usage from OCR text."""
    # Adjust regex patterns based on your specific bill format
    usage_patterns = [
        r'(?:Usage|Consumption|Water Usage)[:\s]+(\d+\.?\d*)',
        r'(\d+\.?\d*)\s*(?:gallons|gal|CCF|HCF|m³|cubic \w+)'
    ]
    
    for pattern in usage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
    
    return None

def extract_cost(text):
    """Extract cost from OCR text."""
    # Adjust regex patterns based on your specific bill format
    cost_patterns = [
        r'(?:Total|Amount Due|Balance)[:\s]+\$?(\d+\.?\d*)',
        r'\$\s*(\d+\.?\d*)'
    ]
    
    for pattern in cost_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
    
    return None