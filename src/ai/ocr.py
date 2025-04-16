import cv2
import pytesseract
import re
from datetime import datetime
from pathlib import Path

from models.bill_data import BillData
from ai.image_processor import preprocess_image

# Configure pytesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Uncomment and adjust for Windows

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
    
    print("===== RAW OCR TEXT =====")
    print(text)
    print("========================")
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
    # Expand regex patterns based on your specific bill format
    usage_patterns = [
        # Standard patterns
        r'(?:Usage|Consumption|Water Usage)[:\s]+(\d+\.?\d*)',
        r'(\d+\.?\d*)\s*(?:gallons|gal|CCF|HCF|m³|cubic \w+)',
        
        # Handle OCR errors for "Consumption"
        r'(?:Sonsumption|[Cc]ons[uo]mpt[il]on)[^\n]*?(\d+)',
        
        # Pattern specifically for the format in your bill
        r'(?:Read|Bead)[^\n]*?(?:Sonsumption|[Cc]ons[uo]mpt[il]on)[^\n]*?(\d+)',
        
        # Look for consumption in the account activity section
        r'ACCOUNT ACTIVITY[^\n]*?(\d{3,4})',
        
        # Look for numbers after dates (often consumption values)
        r'\d{2}[/-]\d{2}[/-]\d{2,4}[^\n\d]*(\d+)',
        
        # More general patterns to catch consumption values
        r'(?:current|meter)[^\n]*?(\d{3,5})',
        r'(\d{3,5})\s*(?:gal|gallons)?$',  # Numbers at the end of lines
        
        # Very specific pattern for your bill format
        r'2\d{3}\s+\d{4}\s+(\d{3,5})',  # Pattern like "2103 2065 3800"
    ]
    
    for pattern in usage_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                # Clean up the match by removing commas
                usage_str = match.replace(',', '')
                value = float(usage_str)
                # Filter out very small values that might be meter readings
                if value >= 100:  # Assume water usage is at least 100 gallons/units
                    return value
            except (ValueError, TypeError):
                continue
    
    # If we get here, try a more desperate approach: find all numbers and pick likely candidates
    all_numbers = re.findall(r'(\d{3,5})', text)  # Look for 3-5 digit numbers
    
    # Filter and sort numbers by likelihood of being consumption values
    candidates = []
    for num in all_numbers:
        try:
            value = float(num)
            # Typical water consumption values might be in hundreds or thousands
            if 100 <= value <= 10000:
                candidates.append(value)
        except ValueError:
            continue
    
    # Return the most likely candidate, if any
    if candidates:
        # Return the median value as a simple heuristic
        candidates.sort()
        return candidates[len(candidates) // 2]
    
    return None

def extract_cost(text):
    """Extract cost from OCR text."""
    # Adjust regex patterns based on your specific bill format
    cost_patterns = [
        r'(?:Total|Amount Due|Balance|CURRENT CHARGES)[:\s]+\$?(\d+\.?\d*)',
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