import pathlib
from google.genai import types
from google.genai import Client # Imported for type hint in function signature

MODEL_NAME = "gemini-2.0-flash"

def ask_gemini_about_pdf(client: Client, user_question: str, pdf_filepath: pathlib.Path) -> str:
    """
    Asks the Gemini model a question about the content of a PDF file.

    Args:
        client: The initialized genai.Client object.
        user_question: The question to ask.
        pdf_filepath: The pathlib.Path object pointing to the PDF file.

    Returns:
        The text response from the Gemini model.
    """
    # Read the content of the PDF file into bytes
    pdf_content_bytes = pdf_filepath.read_bytes()

    # Construct the `contents` list for the Gemini model
    contents = [
        types.Part.from_bytes(
            data=pdf_content_bytes,
            mime_type='application/pdf',
        ),
        user_question
    ]

    # Call `client.models.generate_content`
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

    # Return the text response from the model
    return response.text

def extract_market_research_findings(client: Client, pdf_filepath: pathlib.Path) -> str:
    """
    Analyzes the provided PDF content using the Gemini model to extract and summarize
    key market research findings, insights, and trends presented in the document.

    Args:
        client: The initialized genai.Client object.
        pdf_filepath: The pathlib.Path object pointing to the PDF file.

    Returns:
        A summarized text of key market research findings, insights, and trends.
    """
    # Read the content of the PDF file into bytes
    pdf_content_bytes = pdf_filepath.read_bytes()

    # Construct a clear and specific prompt
    prompt = 'Summarize the key market research findings, insights, and trends presented in this document.'

    # Create a `contents` list
    contents = [
        types.Part.from_bytes(
            data=pdf_content_bytes,
            mime_type='application/pdf',
        ),
        prompt
    ]

    # Call `client.models.generate_content`
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

    # Return the text response from the model
    return response.text

def extract_structured_data_from_pdf(client: Client, pdf_filepath: pathlib.Path, extraction_prompt: str) -> str:
    """
    Extracts structured data from a PDF file using the Gemini model based on a given prompt.

    Args:
        client: The initialized genai.Client object.
        pdf_filepath: The pathlib.Path object pointing to the PDF file.
        extraction_prompt: A string containing instructions for the Gemini model on what structured
                           data to extract and in what format (e.g., JSON).

    Returns:
        A string representing the extracted structured data (e.g., a JSON string).
    """
    # Inside the function, read the content of the PDF file into bytes
    pdf_content_bytes = pdf_filepath.read_bytes()

    # Construct the `contents` list for the Gemini model
    contents = [
        types.Part.from_bytes(
            data=pdf_content_bytes,
            mime_type='application/pdf',
        ),
        extraction_prompt
    ]

    # Call `client.models.generate_content` with the specified model and contents
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

    # Return the text response from the model
    return response.text