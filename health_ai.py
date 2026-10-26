
import os
import streamlit as st
from google import genai


def generate_health_remarks(glucose, haemoglobin, cholesterol):
    """
    Generate cautious, non-diagnostic remarks
    from the three supplied blood-test values.
    """

    # Read the API key from Streamlit secrets or environment
    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY", "")
    )

    if not api_key:
        return (
            "AI remarks unavailable: API key is not configured. "
            "Please review the test results with a healthcare professional."
        )

    # Create the Gemini API client
    client = genai.Client(api_key=api_key)

    # Ask the AI to comment cautiously on the values
    prompt = f"""
    You are generating educational remarks for a software assessment.

    Blood-test values supplied:
    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Explain cautiously whether any values may merit review.
    Mention that interpretation depends on units, reference ranges,
    fasting status, age, sex, medical history and clinical context.

    Do not diagnose a disease.
    Do not prescribe medication or recommend treatment changes.
    Do not invent missing information.
    Keep the response concise and understandable.
    State that a qualified healthcare professional must interpret
    the results.

    These remarks are educational and are not medical advice.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "AI did not return any remarks. Please try again."

    
    except Exception as error:
        return (
            f"AI request failed: {type(error).__name__}: {error}"
        )
