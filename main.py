import pytesseract
from PIL import Image
import json
import psycopg2
import os
import re
from pdf2image import convert_from_path

# Configure Tesseract OCR path (modify based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """ Convert image to grayscale and apply thresholding for better OCR accuracy. """
    img = Image.open(image_path).convert('L')
    return img

def extract_text(image):
    """ Use Tesseract OCR to extract text from an image. """
    return pytesseract.image_to_string(image)

def parse_extracted_text(text):
    """ Extract relevant information from OCR output using regex. """
    data = {}
    
    # Extract patient details
    data['patient_name'] = re.search(r'Name:\s*(.+)', text).group(1) if re.search(r'Name:\s*(.+)', text) else "Unknown"
    data['dob'] = re.search(r'DOB:\s*(\d{2}/\d{2}/\d{4})', text).group(1) if re.search(r'DOB:\s*(\d{2}/\d{2}/\d{4})', text) else "Unknown"
    data['date'] = re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text).group(1) if re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text) else "Unknown"
    
    # Extract treatment details
    data['injection'] = "Yes" if "Injection: Yes" in text else "No"
    data['exercise_therapy'] = "Yes" if "Exercise Therapy: Yes" in text else "No"
    
    # Extract difficulty ratings
    difficulty_ratings = {}
    for category in ["bending", "putting on shoes", "sleeping"]:
        match = re.search(fr'{category}:\s*(\d+)', text, re.IGNORECASE)
        difficulty_ratings[category.replace(" ", "_")] = int(match.group(1)) if match else 0
    data['difficulty_ratings'] = difficulty_ratings
    
    # Extract patient changes
    patient_changes = {}
    for category in ["since last treatment", "since start of treatment", "last 3 days"]:
        match = re.search(fr'{category}:\s*(\w+)', text, re.IGNORECASE)
        patient_changes[category.replace(" ", "_")] = match.group(1) if match else "Unknown"
    data['patient_changes'] = patient_changes
    
    # Extract pain symptoms
    pain_symptoms = {}
    for symptom in ["pain", "numbness", "tingling", "burning", "tightness"]:
        match = re.search(fr'{symptom}:\s*(\d+)', text, re.IGNORECASE)
        pain_symptoms[symptom] = int(match.group(1)) if match else 0
    data['pain_symptoms'] = pain_symptoms
    
    # Extract medical assistant data
    medical_assistant_data = {}
    for field in ["blood pressure", "hr", "weight", "height", "spo2", "temperature", "blood glucose", "respirations"]:
        match = re.search(fr'{field}:\s*([\w/\'.]+)', text, re.IGNORECASE)
        medical_assistant_data[field.replace(" ", "_")] = match.group(1) if match else "Unknown"
    data['medical_assistant_data'] = medical_assistant_data
    
    return data

def store_data_in_db(json_data):
    """ Store extracted JSON data in a PostgreSQL database. """
    conn = psycopg2.connect(
        dbname='medical_records', user='postgres', password='password', host='localhost', port='5432'
    )
    cur = conn.cursor()
    
    cur.execute("INSERT INTO patients (name, dob) VALUES (%s, %s) RETURNING id;", (json_data['patient_name'], json_data['dob']))
    patient_id = cur.fetchone()[0]
    
    cur.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s);", (patient_id, json.dumps(json_data)))
    conn.commit()
    cur.close()
    conn.close()

def process_file(file_path):
    """ Process an image or PDF file to extract and store data. """
    if file_path.lower().endswith('.pdf'):
        images = convert_from_path(file_path)
        text = " ".join([extract_text(preprocess_image(img)) for img in images])
    else:
        text = extract_text(preprocess_image(file_path))
    
    json_data = parse_extracted_text(text)
    store_data_in_db(json_data)
    
    print("Extracted JSON Data:")
    print(json.dumps(json_data, indent=4))

# Example usage
if __name__ == "__main__":
    process_file('patient_form.jpg')
