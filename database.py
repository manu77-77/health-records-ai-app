
import sqlite3

# Name of the database file
DATABASE_NAME = "health_records.db"


# Create the database table if it does not exist
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


# Save one patient record
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

# Get all saved patient records
def get_patients():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "SELECT * FROM patients ORDER BY id"
    )

    patients = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return patients

# Update the email address of one patient
def update_patient_email(patient_id, new_email):

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "UPDATE patients SET email = ? WHERE id = ?",
        (new_email, patient_id)
    )

    connection.commit()
    connection.close()


# Delete one patient record
def delete_patient(patient_id):

    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()
