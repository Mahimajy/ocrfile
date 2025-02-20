import pytesseract
import cv2
import json
import psycopg2
from pdf2image import convert_from_path
from database import insert_patient_data

# Function to preprocess images
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# Function to extract text using Tesseract OCR
def extract_text(image_path):
    image = preprocess_image(image_path)
    return pytesseract.image_to_string(image)

# Function to process PDFs
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"
    return extracted_text

# Function to structure extracted data into JSON
def structure_data(text):
    # Example: Extracting patient name and details (custom logic needed)
    data = {
        "patient_name": "John Doe",
        "dob": "01/05/1988",
        "date": "02/06/2025",
        "injection": "Yes",
        "exercise_therapy": "No",
        "difficulty_ratings": {"bending": 3, "putting_on_shoes": 1, "sleeping": 2},
        "pain_symptoms": {"pain": 2, "numbness": 5, "tingling": 6, "burning": 7, "tightness": 5},
        "medical_assistant_data": {
            "blood_pressure": "120/80",
            "hr": 80,
            "weight": 67,
            "height": "5'7",
            "spo2": 98,
            "temperature": "98.6",
            "blood_glucose": 115,
            "respirations": 16,
        },
    }
    return json.dumps(data, indent=4)

# Main execution
if __name__ == "__main__":
    input_path = input("Enter the image file path: ").strip()
  # Change to actual path
    extracted_text = extract_text(input_path)
    structured_json = structure_data(extracted_text)

    # Save JSON
    with open("sample_output.json", "w") as f:
        f.write(structured_json)

    # Store in Database
    insert_patient_data(structured_json)
    print("Data successfully extracted and stored!")
