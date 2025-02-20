import sqlite3

def connect_db():
    return sqlite3.connect("patients.db")  # Ensure this matches your database name

def insert_patient_data(data):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients (name, dob, age, diagnosis)
        VALUES (?, ?, ?, ?)
    """, (data["patient_name"], data["dob"], data["age"], data["diagnosis"]))

    conn.commit()
    conn.close()

