from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class BillData:
    """Data structure for storing extracted water bill information."""
    
    date: date
    usage: float  # Water usage in gallons/liters
    cost: float   # Total cost
    
    # Optional fields
    account_number: Optional[str] = None
    billing_period: Optional[str] = None
    
    def __str__(self):
        return f"Date: {self.date}, Usage: {self.usage}, Cost: {self.cost}"