# Health Records AI App

A Python Streamlit application for managing patient health records with SQLite storage and AI-generated educational remarks.

## Features
- Create, read, update, and delete patient records
- Validate email addresses and dates of birth
- Validate glucose, haemoglobin, and cholesterol values
- Store records persistently using SQLite
- Generate educational health remarks using Google's Gemini API
- Display a disclaimer that AI remarks are not a medical diagnosis

## Technologies
- Python
- Streamlit
- SQLite
- Google Gemini API

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create `.streamlit/secrets.toml` and add your own Gemini API key:

   `GEMINI_API_KEY = "your_api_key_here"`

5. Run the application:

   `streamlit run app.py`

## Security
Never commit API keys, secrets files, virtual environments, or local database files.

## Disclaimer
This application is an educational prototype and does not provide medical diagnoses or replace professional medical advice.
