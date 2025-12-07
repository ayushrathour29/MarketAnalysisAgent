import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pathlib
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from agents.gemini_utils import (
    ask_gemini_about_pdf,
    extract_market_research_findings,
    extract_structured_data_from_pdf,
    router_agent_call
)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR")

filepath = pathlib.Path("./data/IncAI.pdf")


embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
print(f"RAG Vector Store loaded from {VECTOR_DB_DIR}.")






# def run_market_analyst_agent():
#   """
#   Integrates the Q&A, Market Research Findings, and Structured Data Extraction functions
#   into a cohesive agent with an interactive command-line interface.
#   """
#   print("Welcome to the AI Market Analyst Agent!")
#   while True:
#     print("\nChoose an action:")
#     print("1. Ask a question about the PDF")
#     print("2. Get market research summary")
#     print("3. Extract structured data")
#     print("4. Exit")

#     choice = input("Enter your choice (1-4): ")

#     if choice == '1':
#       user_question = input("Enter your question: ")
#       answer = ask_gemini_about_pdf(client, user_question, vectorstore)
#       print("\n--- Answer ---")
#       print(answer)
#       print("--------------")
#     elif choice == '2':
#       print("\n--- Market Research Summary ---")
#       summary = extract_market_research_findings(client, filepath)
#       print(summary)
#       print("-------------------------------")
#     elif choice == '3':
#       extraction_prompt = input("Enter your extraction prompt (e.g., 'Extract company names and market shares as JSON'): ")
#       print("\n--- Structured Data ---")
#       structured_data = extract_structured_data_from_pdf(client, filepath, extraction_prompt)
#       print(structured_data)
#       print("-------------------------")
#     elif choice == '4':
#       print("Exiting AI Market Analyst Agent. Goodbye!")
#       break
#     else:
#       print("Invalid choice. Please enter a number between 1 and 4.")

# # Call the main function to start the interactive agent
# if __name__ == "__main__":
#   run_market_analyst_agent()


def unified_agent_call(user_query: str):
    """
    The main Gradio function that routes the query to the correct tool.
    """
    if client is None or vectorstore is None:
        return "ERROR: Agent resources are not initialized. Check your GOOGLE_API_KEY and ensure you have run 'python setup_rag.py'."

    # 1. Router decides tool_name
    tool_name = router_agent_call(client, user_query)
    
    # Provide visual feedback on routing
    print(f"Routing Query: '{user_query}' -> Tool: {tool_name}")

    try:
        # 2. Route to the correct function
        if tool_name == "QA":
            # Uses RAG
            result = ask_gemini_about_pdf(client, user_query, vectorstore)
            return f"🤖 **Tool Used: Q&A (RAG Retrieval)**\n\n{result}"
            
        elif tool_name == "SUMMARIZE":
            # Uses Full Context
            result = extract_market_research_findings(client, filepath)
            return f"🤖 **Tool Used: Summary (Full Context)**\n\n{result}"
            
        elif tool_name == "EXTRACT":
            # Uses Full Context
            # For extraction, the full user query is the extraction prompt
            result = extract_structured_data_from_pdf(client, filepath, user_query)
            return f"🤖 **Tool Used: Structured Extraction (Full Context)**\n\n{result}"
            
        else:
            return f"🤖 **Tool Used: Fallback**\n\nCould not determine the appropriate tool for the query. Router chose: {tool_name}. Please rephrase your question."

    except Exception as e:
        return f"An error occurred while running the selected tool: {e}"

# --- Gradio Interface Definition ---

if __name__ == "__main__":
  demo = gr.Interface(
     fn=unified_agent_call,
     inputs=gr.Textbox(
        lines=3,
        placeholder="Ask a specific question (QA), request a general summary (SUMMARIZE), or ask for data extraction (EXTRACT)...",
        label="Your Query (Autonomous Agent)"
      ),
        
      outputs=gr.Textbox(
         label="AI Market Analyst Response",
      ),
      
      title="🤖 AI Market Analyst (Autonomous Router Demo)",
      description="Enter a query and the agent will autonomously decide whether to perform Q&A (RAG), Summarization, or Data Extraction."
  )        
        # Launch the Gradio app
        # The `share=True` option creates a public link for easy sharing (good for testing/demo)
demo.launch(inbrowser=True)