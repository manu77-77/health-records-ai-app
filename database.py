
import sqlite3

DATABASE_NAME = "health_records.db"

def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT DEFAULT ''
        )
    """)

    connection.commit()
    connection.close()


def add_patient(
    name, dob, email,
    glucose, haemoglobin, cholesterol,
    remarks=""
):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute("""
        INSERT INTO patients (
            full_name, date_of_birth, email,
            glucose, haemoglobin, cholesterol, remarks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name, dob, email,
        glucose, haemoglobin, cholesterol, remarks
    ))

    connection.commit()
    connection.close()

def get_patients():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "SELECT * FROM patients ORDER BY id"
    )

    patients = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return patients

def update_patient_email(patient_id, new_email):

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "UPDATE patients SET email = ? WHERE id = ?",
        (new_email, patient_id)
    )

    connection.commit()
    connection.close()


def delete_patient(patient_id):

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()
