import pathlib
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from google.genai import Client

# Configuration
VECTOR_DB_DIR = "./chroma_db"
EMBEDDING_MODEL = "models/gemini-embedding-001"
CHUNK_SIZE = 500  
CHUNK_OVERLAP = 50 

def create_vector_store(client: Client, pdf_filepath: pathlib.Path) -> Chroma:
    """
    Handles the entire RAG ingestion pipeline: Load -> Chunk -> Embed -> Store.
    
    Args:
        client: The initialized genai.Client object.
        pdf_filepath: The pathlib.Path object pointing to the PDF file.
        
    Returns:
        The initialized Chroma vector store object.
    """
    print(f"--- Starting RAG Ingestion for {pdf_filepath.name} ---")
    
    # 1. Load the document
    loader = PyPDFLoader(str(pdf_filepath))
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF.")

    # 2. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # 3. Embed the chunks
    # Note: GoogleGenerativeAIEmbeddings automatically uses GOOGLE_API_KEY env var
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    print(f"Using Embedding Model: {EMBEDDING_MODEL}")

    # 4. Store the vectors in ChromaDB (persistent)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )
    vectorstore.persist()
    print(f"Successfully created and persisted vector store to {VECTOR_DB_DIR}/")
    
    return vectorstore

if __name__ == "__main__":
    # Example usage: Replace with your actual client initialization and path
    # from google.colab import userdata # Use os.getenv("GOOGLE_API_KEY") locally

    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Please set the GOOGLE_API_KEY environment variable.")
            exit()
        client = Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing client: {e}")
        exit()

    filepath = pathlib.Path("./data/IncAI.pdf")
    if not filepath.exists():
        print(f"Error: PDF file not found at {filepath.resolve()}.")
        exit()

    # Create or load the vector store
    if os.path.exists(VECTOR_DB_DIR):
        print(f"Vector store already exists at {VECTOR_DB_DIR}. Skipping ingestion.")
        # Load the existing store (using the same embedding model for consistency)
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    else:
        vectorstore = create_vector_store(client, filepath)
        
    print("RAG setup complete. You can now run main.py.")