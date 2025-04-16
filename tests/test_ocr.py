import unittest
from src.ai.ocr import OCRProcessor

class TestOCRProcessor(unittest.TestCase):
    def setUp(self):
        self.ocr_processor = OCRProcessor()

    def test_extract_text(self):
        # Assuming we have a sample image for testing
        sample_image_path = 'path/to/sample_water_bill.jpg'
        extracted_text = self.ocr_processor.extract_text(sample_image_path)
        
        # Check if the extracted text contains expected keywords
        self.assertIn('Date', extracted_text)
        self.assertIn('Usage', extracted_text)
        self.assertIn('Cost', extracted_text)

if __name__ == '__main__':
    unittest.main()