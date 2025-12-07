```markdown
# AI Market Analyst Agent

## Project Description

This project provides an AI Market Analyst Agent designed to interact with PDF documents. Leveraging Google's Gemini API, it offers three core functionalities:
1.  **Question & Answer (Q&A):** Ask specific questions about the content of a PDF and get direct answers.
2.  **Market Research Summarization:** Obtain a comprehensive summary of market research findings, insights, and trends from a PDF document.
3.  **Structured Data Extraction:** Extract specific structured data (e.g., company names, market shares) from PDFs in a desired format, such as JSON.

## Setup Instructions

Follow these steps to set up and run the AI Market Analyst Agent locally:

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   A Google Cloud Project with the Gemini API enabled and an API Key.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd AI-Market-Analyst-Agent
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Google API Key:**
    Create a `.env` file in the root directory of the project based on `.env.example` and add your Google API Key:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```
    Replace `YOUR_GOOGLE_API_KEY` with your actual API key.

## How to Run the Agent

After completing the setup, you can run the interactive command-line interface (CLI) of the agent:

1.  **Ensure your virtual environment is active.**
2.  **Execute the main CLI script:**
    ```bash
    python main.py
    ```
3.  The agent will present a menu with options (Q&A, Market Research Summary, Structured Data Extraction, Exit). Follow the prompts to interact with the agent.

## Project Structure

The project is organized into the following directories and files:

*   `agents/`:
*    `gemini_utils.py`
    *   `ask_gemini_about_pdf`: Contains the function for answering questions about PDF content.
    *   `extract_market_research_findings`: Implements the function for summarizing market research from PDFs.
    *   `extract_structured_data_from_pdf`: Provides the function for extracting structured data from PDFs.
*   
    *   `main.py`: The main script that provides the interactive command-line interface for the agent, integrating functions from the `agents` directory.
*   
    *   `.env.example`: A template file showing how to set up environment variables, specifically the `GOOGLE_API_KEY`.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `.gitignore`: Specifies files and directories to be ignored by Git.
*   `README.md`: This file, providing an overview and instructions for the project.

## Functionalities

The AI Market Analyst Agent offers the following capabilities:

*   **Ask a question about the PDF:** Users can input a natural language question, and the agent will use the Gemini model to find and provide a relevant answer based on the PDF's content.
*   **Get market research summary:** With a single command, the agent processes the PDF to identify and summarize key market research findings, including market size, growth, competitive landscape, and SWOT analysis.
*   **Extract structured data:** Users can provide a specific prompt detailing the desired structured data (e.g., company names, market shares, current and projected market sizes) and the output format (e.g., JSON), and the agent will extract and present the information accordingly.
```


## working of code
Welcome to the AI Market Analyst Agent!

Choose an action:
1. Ask a question about the PDF
2. Get market research summary
3. Extract structured data
4. Exit
Enter your choice (1-4): 1
Enter your question: How it gives service to the public?

--- Answer ---
Based on the text provided, Innovate Inc. serves the public by offering enterprise-level AI workflow automation software. This software, particularly their flagship product "Automata Pro," helps businesses, especially those in logistics and supply chain, to increase efficiency and reduce operational costs. This in turn can lead to lower prices or better service for the end consumer. Additionally, the company's expansion into sectors like healthcare can lead to improvements in those fields, ultimately benefiting the public.

--------------

Choose an action:
1. Ask a question about the PDF
2. Get market research summary
3. Extract structured data
4. Exit
Enter your choice (1-4): 3


Enter extraction_prompt: Extract the company names, their market shares, the current market size (in billions), and the projected market size by 2030 (in billions) from this document. Present the information as a JSON object with keys like "companies" (an array of objects with "name" and "market_share" keys), "current_market_size", and "projected_market_size_2030".


		```json
		{
		  "companies": [
		    {
		      "name": "Innovate Inc.",
		      "market_share": "12%"
		    },
		    {
		      "name": "Synergy Systems",
		      "market_share": "18%"
		    },
		    {
		      "name": "FutureFlow",
		      "market_share": "15%"
		    },
		    {
		      "name": "QuantumLeap",
		      "market_share": "3%"
		    }
		  ],
		  "current_market_size": 15,
		  "projected_market_size_2030": 40
		}
		```

--------------

Choose an action:
1. Ask a question about the PDF
2. Get market research summary
3. Extract structured data
4. Exit
Enter your choice (1-4): 3
Exiting AI Market Analyst Agent. Goodbye!