DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    age INTEGER,
    diagnosis TEXT
);
