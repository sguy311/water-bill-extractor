import os
import pandas as pd
from pathlib import Path
from models.bill_data import BillData

def add_to_spreadsheet(bill_data, output_file):
    """Add bill data to an Excel spreadsheet."""
    
    # Create a new dataframe with the bill data
    new_data = {
        'Date': [bill_data.date],
        'Usage': [bill_data.usage],
        'Cost': [bill_data.cost],
        'Account Number': [bill_data.account_number or ''],
        'Billing Period': [bill_data.billing_period or '']
    }
    
    new_row = pd.DataFrame(new_data)
    
    # Check if file exists
    if os.path.exists(output_file):
        # Load existing data
        try:
            df = pd.read_excel(output_file)
            
            # Append new data
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Sort by date
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values(by='Date')
            
            # Write back to file
            df.to_excel(output_file, index=False)
            
        except Exception as e:
            print(f"Error updating spreadsheet: {e}")
            # Create new file with just this data
            new_row.to_excel(output_file, index=False)
    else:
        # Create new file with just this data
        new_row.to_excel(output_file, index=False)