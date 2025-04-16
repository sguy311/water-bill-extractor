# Water Bill Extractor

This project is an application that utilizes AI to extract date, usage, and cost information from a photo of a water bill and adds it to a spreadsheet. 

## Features

- Optical Character Recognition (OCR) to extract text from images of water bills.
- Image preprocessing to enhance the quality of the input images for better OCR results.
- Integration with spreadsheet software to store the extracted data.

## Project Structure

```
water-bill-extractor
├── src
│   ├── main.py                # Entry point of the application
│   ├── ai
│   │   ├── __init__.py        # Initializes the AI module
│   │   ├── ocr.py             # Contains OCRProcessor class for text extraction
│   │   └── image_processor.py  # Contains ImageProcessor class for image preprocessing
│   ├── data
│   │   ├── __init__.py        # Initializes the data module
│   │   └── spreadsheet_manager.py # Contains SpreadsheetManager class for managing spreadsheet data
│   ├── models
│   │   ├── __init__.py        # Initializes the models module
│   │   └── bill_data.py       # Defines BillData class for extracted data representation
│   └── utils
│       ├── __init__.py        # Initializes the utils module
│       └── helpers.py         # Contains utility functions for various tasks
├── tests
│   ├── __init__.py            # Initializes the tests module
│   ├── test_ocr.py            # Unit tests for OCRProcessor class
│   └── test_spreadsheet.py     # Unit tests for SpreadsheetManager class
├── requirements.txt            # Lists project dependencies
├── setup.py                   # Configuration file for packaging the application
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/water-bill-extractor.git
   cd water-bill-extractor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place the image of the water bill in the appropriate directory.
2. Run the application:
   ```
   python src/main.py
   ```

3. Follow the prompts to extract data and add it to the spreadsheet.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.