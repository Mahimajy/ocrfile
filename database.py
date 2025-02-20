import psycopg2
import json

# Database connection
def connect_db():
    return psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )

# Insert patient data into the database
def insert_patient_data(json_data):
    conn = connect_db()
    cursor = conn.cursor()

    data = json.loads(json_data)
    cursor.execute("INSERT INTO patients (name, dob) VALUES (%s, %s) RETURNING id;",
                   (data["patient_name"], data["dob"]))
    patient_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s);",
                   (patient_id, json_data))

    conn.commit()
    cursor.close()
    conn.close()
