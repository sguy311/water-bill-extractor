import unittest
from src.data.spreadsheet_manager import SpreadsheetManager

class TestSpreadsheetManager(unittest.TestCase):
    def setUp(self):
        self.manager = SpreadsheetManager()
        self.test_date = "2023-10-01"
        self.test_usage = 150
        self.test_cost = 45.75

    def test_add_data(self):
        result = self.manager.add_data(self.test_date, self.test_usage, self.test_cost)
        self.assertTrue(result)
        # Additional checks can be added here to verify the data in the spreadsheet

if __name__ == '__main__':
    unittest.main()