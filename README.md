# OCR-Based Text Extraction and Database Storage

This project extracts text from scanned documents using **Tesseract OCR**, structures the extracted data into **JSON format**, and stores it in an **SQLite database**.

---

## Features
✔ Extracts text from images using **Tesseract OCR**  
✔ Converts extracted text into a structured **JSON format**  
✔ Stores patient details in an **SQLite database**  
✔ Supports querying stored patient records  

---

## Installation

### **1. Install Dependencies**  
Ensure you have Python installed, then install the required libraries:  
```sh
pip install opencv-python pytesseract sqlite3
```

### **2. Install Tesseract OCR**  
Download and install **Tesseract OCR** from:  
🔗 [Tesseract OCR Download](https://github.com/UB-Mannheim/tesseract/wiki)  

After installation, update the Tesseract path in `ocr_extraction.py`:  
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## **Usage**

### **1. Place Image Files**  
Place scanned form images in the `data/` folder. Example:  
```
data/sample_form.jpg
```

### **2. Run the OCR Script**  
```sh
python ocr_extraction.py
```

---

## **Contributing**
Feel free to contribute by submitting issues or pull requests in the GitHub repository.

---

## **Author**
[👤 Mahimajy](https://github.com/Mahimajy)  
📧 mahimajy@gmail.com

