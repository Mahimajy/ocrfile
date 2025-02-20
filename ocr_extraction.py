import os
import cv2
import pytesseract
import sqlite3
from database import insert_patient_data
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract text from an image
def extract_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    return text

# Function to structure extracted text
def process_text(text):
    lines = text.split("\n")
    structured_data = {"patient_name": "Unknown", "dob": None, "age": None, "diagnosis": "Not Provided"}

    for line in lines:
        if "Name:" in line:
            structured_data["patient_name"] = line.split(":")[-1].strip()
        elif "DOB:" in line:  # Extract Date of Birth
            structured_data["dob"] = line.split(":")[-1].strip()
        elif "Age:" in line:
            structured_data["age"] = int(line.split(":")[-1].strip())
        elif "Diagnosis:" in line:
            structured_data["diagnosis"] = line.split(":")[-1].strip()

    return structured_data

# Run the OCR pipeline
image_path = "data/sample_form.jpg"  # Update with correct path
extracted_text = extract_text(image_path)
structured_data = process_text(extracted_text)

# Insert into database
insert_patient_data(structured_data)

print("Data successfully inserted into SQLite database.")

