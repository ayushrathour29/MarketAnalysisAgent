import pathlib
from google.genai import types
from google.genai import Client
from langchain_community.vectorstores import Chroma

MODEL_NAME = "gemini-2.5-flash"


ROUTER_PROMPT = """
You are an intelligent task router for a Market Analyst Agent.
Your job is to classify the user's query and decide which tool should be used to provide the best answer.

The three possible tools are:
1. QA: Use this if the user asks a specific question about content, facts, or data (e.g., "What is the market share of X?", "Explain the challenge on page 5").
2. SUMMARIZE: Use this if the user asks for a high-level overview, synthesis, or simplification (e.g., "Summarize the findings of the report", "Give me a general overview").
3. EXTRACT: Use this if the user asks for structured data, a list, or a table, or asks to output the result as JSON (e.g., "Extract all company names and their valuations as a JSON list", "List the key risks").

Based on the user's query, output ONLY the single, capitalised word for the chosen tool. Do not add any other text, explanation, or punctuation.

User Query: {user_query}
Tool Choice:
"""

def router_agent_call(client: Client, user_query: str) -> str:
    """
    Uses Gemini to classify the user's intent and return the correct tool name.
    
    Returns:
        One of: 'QA', 'SUMMARIZE', or 'EXTRACT'
    """
    contents = [
        ROUTER_PROMPT.format(user_query=user_query)
    ]
   
    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.0
        )
    )
    
    # Clean up the output to ensure only the tool name is returned
    return response.text.strip().upper()


RAG_PROMPT_TEMPLATE = """
You are an expert market analyst. Use ONLY the following retrieved context to answer the user's question. 
If the information is not present in the context, state clearly that you cannot answer based on the provided data.

CONTEXT:
---
{context}
---

QUESTION: {question}
ANSWER:
"""

def ask_gemini_about_pdf(client: Client, user_question: str, vectorstore: Chroma) -> str:
    """
    Asks the Gemini model a question about the content of a PDF file.

    Args:
        client: The initialized genai.Client object.
        user_question: The question to ask.
        pdf_filepath: The pathlib.Path object pointing to the PDF file.

    Returns:
        The text response from the Gemini model.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4}) # Retrieve Top 4 relevant chunks
    retrieved_docs = retriever.invoke(user_question)
    
    # Concatenate the content of the retrieved documents
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # 2. Construct the final RAG prompt
    final_prompt = RAG_PROMPT_TEMPLATE.format(
        context=context_text,
        question=user_question
    )

    # 3. Generation
    contents = [final_prompt]
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

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