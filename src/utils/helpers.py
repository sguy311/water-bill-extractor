def format_date(date_str):
    # Function to format the date string into a standard format
    from datetime import datetime
    
    try:
        # Attempt to parse the date string
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # Handle the case where the date string is not in the expected format
        return None

def validate_usage_cost(usage, cost):
    # Function to validate that usage and cost are positive numbers
    try:
        usage = float(usage)
        cost = float(cost)
        return usage >= 0 and cost >= 0
    except ValueError:
        return False

def handle_exception(e):
    # Function to handle exceptions and log errors
    import logging
    
    logging.error(f"An error occurred: {str(e)}")