from setuptools import setup, find_packages

setup(
    name='water-bill-extractor',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='An application to extract date usage and cost from a photo of a water bill and add it to a spreadsheet.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytesseract',
        'Pillow',
        'openpyxl',
        'numpy',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'water-bill-extractor=main:main',
        ],
    },
)