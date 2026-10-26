import streamlit as st
import re
from datetime import datetime, date

from database import (
    initialize_database,
    add_patient,
    get_patients,
    update_patient_email,
    delete_patient,
)
from health_ai import generate_health_remarks

initialize_database()

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

st.set_page_config(
    page_title="Health Records App",
    layout="wide"
)

st.title("Health Records App")
st.header("Add Patient")

with st.form("patient_form"):

    full_name = st.text_input("Full Name")

    date_of_birth = st.text_input(
        "Date of Birth (DD.MM.YYYY)",
        placeholder="28.01.1960"
    )

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose", min_value=0.0, value=0.0, step=1.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin", min_value=0.0, value=0.0, step=0.1
    )

    cholesterol = st.number_input(
        "Cholesterol", min_value=0.0, value=0.0, step=1.0
    )

    submitted = st.form_submit_button("Validate and Save")

if submitted:

    errors = []

    if not full_name.strip():
        errors.append("Full name is required.")


    if not re.fullmatch(email_pattern, email.strip()):
        errors.append("Enter a valid email address.")

    try:
        birth_date = datetime.strptime(
            date_of_birth.strip(), "%d.%m.%Y"
    ).date()

        if birth_date > date.today():
            errors.append("Date of birth cannot be in the future.")

    except ValueError:
        errors.append("Enter a real date in DD.MM.YYYY format.")

    if glucose <= 0:
        errors.append("Glucose must be greater than zero.")

    if haemoglobin <= 0:
        errors.append("Haemoglobin must be greater than zero.")

    if cholesterol <= 0:
        errors.append("Cholesterol must be greater than zero.")

    
    if errors:
        st.error("Please correct these problems:")

        for error in errors:
            st.write("- ", error)

    else:
        with st.spinner("Generating AI remarks..."):
            remarks = generate_health_remarks(
                glucose,
                haemoglobin,
                cholesterol
            )

        add_patient(
            full_name.strip(),
            birth_date.strftime("%d.%m.%Y"),
            email.strip(),
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )

        st.success("Patient record saved successfully!")
        st.subheader("AI-Generated Remarks")
        st.write(remarks)



st.header("Saved Patient Records")

patients = get_patients()

if patients:
    st.dataframe(patients, use_container_width=True)

    st.header("Update Patient Email")

    selected_id = st.selectbox(
        "Choose a patient to edit",
        [patient["id"] for patient in patients],
        format_func=lambda patient_id: next(
            patient["full_name"] + " (ID " + str(patient["id"]) + ")"
            for patient in patients
            if patient["id"] == patient_id
        )
    )

    selected_patient = next(
        patient for patient in patients
        if patient["id"] == selected_id
    )

    with st.form("update_form"):

        new_email = st.text_input(
            "New Email Address",
            value=selected_patient["email"]
        )

        update_button = st.form_submit_button("Update Email")

    if update_button:

        if not re.fullmatch(email_pattern, new_email.strip()):
            st.error("Enter a valid email address.")

        else:
            update_patient_email(selected_id, new_email.strip())
            st.success("Email updated successfully!")
            st.rerun()

    st.header("Delete Patient")

    delete_id = st.selectbox(
        "Choose a patient to delete",
        [patient["id"] for patient in patients],
        format_func=lambda patient_id: next(
            patient["full_name"] + " (ID " + str(patient["id"]) + ")"
            for patient in patients
            if patient["id"] == patient_id
        ),
        key="delete_patient_id"
    )

    if st.button("Delete Selected Patient"):

        delete_patient(delete_id)
        st.success("Patient record deleted.")
        st.rerun()

else:
    st.info("No patient records have been saved yet.")
