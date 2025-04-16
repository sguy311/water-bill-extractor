import os
import argparse
from pathlib import Path

from ai.ocr import extract_bill_data
from data.spreadsheet_manager import add_to_spreadsheet
from models.bill_data import BillData

def process_bill_image(image_path, output_spreadsheet):
    """Process a water bill image and add extracted data to a spreadsheet."""
    
    print(f"Processing image: {image_path}")
    
    # Extract data from bill image
    bill_data = extract_bill_data(image_path)
    
    if bill_data:
        # Add extracted data to spreadsheet
        add_to_spreadsheet(bill_data, output_spreadsheet)
        print(f"Successfully added data to {output_spreadsheet}")
        print(f"Date: {bill_data.date}, Usage: {bill_data.usage}, Cost: {bill_data.cost}")
    else:
        print("Failed to extract data from the bill image.")

def main():
    parser = argparse.ArgumentParser(description="Extract data from water bill images")
    parser.add_argument("image_path", help="Path to the water bill image")
    parser.add_argument("--output", "-o", default="water_bills.xlsx", 
                        help="Output spreadsheet file (default: water_bills.xlsx)")
    
    args = parser.parse_args()
    
    # Ensure the image file exists
    if not os.path.isfile(args.image_path):
        print(f"Error: Image file {args.image_path} does not exist.")
        return
    
    process_bill_image(args.image_path, args.output)

if __name__ == "__main__":
    main()