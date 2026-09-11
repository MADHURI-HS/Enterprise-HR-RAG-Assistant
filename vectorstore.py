import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def load_vectorstore():
    documents = []

    # Get correct path to documents folder
    base_dir = os.path.dirname(__file__)
    folder_path = os.path.join(base_dir, "documents")

    # Check if folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError("❌ 'documents' folder not found. Please create it.")

    # Load all PDF files
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # Add metadata (important for enterprise feel)
            for doc in docs:
                doc.metadata["source"] = file

            documents.extend(docs)

    # Check if documents exist
    if len(documents) == 0:
        raise ValueError("❌ No PDF files found inside 'documents' folder.")

    # Split documents into chunks
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings()

    # Create vector database
    vectorstore = Chroma.from_documents(docs, embeddings)

    return vectorstore