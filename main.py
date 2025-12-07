from dotenv import load_dotenv
from google import genai
from google.genai import types
import pathlib
import os
from agents.gemini_utils import (
    ask_gemini_about_pdf,
    extract_market_research_findings,
    extract_structured_data_from_pdf
)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

filepath = pathlib.Path("./data/IncAI.pdf")


# prompt = "Summarize this document"

# response = client.models.generate_content(
#   model="gemini-2.0-flash",
#   contents=[
#       types.Part.from_bytes(
#         data=filepath.read_bytes(),
#         mime_type='application/pdf',
#       ),
#       prompt])






def run_market_analyst_agent():
  """
  Integrates the Q&A, Market Research Findings, and Structured Data Extraction functions
  into a cohesive agent with an interactive command-line interface.
  """
  print("Welcome to the AI Market Analyst Agent!")
  while True:
    print("\nChoose an action:")
    print("1. Ask a question about the PDF")
    print("2. Get market research summary")
    print("3. Extract structured data")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
      user_question = input("Enter your question: ")
      answer = ask_gemini_about_pdf(client, user_question, filepath)
      print("\n--- Answer ---")
      print(answer)
      print("--------------")
    elif choice == '2':
      print("\n--- Market Research Summary ---")
      summary = extract_market_research_findings(client, filepath)
      print(summary)
      print("-------------------------------")
    elif choice == '3':
      extraction_prompt = input("Enter your extraction prompt (e.g., 'Extract company names and market shares as JSON'): ")
      print("\n--- Structured Data ---")
      structured_data = extract_structured_data_from_pdf(client, filepath, extraction_prompt)
      print(structured_data)
      print("-------------------------")
    elif choice == '4':
      print("Exiting AI Market Analyst Agent. Goodbye!")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 4.")

# Call the main function to start the interactive agent
if __name__ == "__main__":
  run_market_analyst_agent()