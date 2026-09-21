# 🏢 Enterprise HR RAG Assistant

An AI-powered Enterprise HR Assistant that allows authenticated users to
ask questions about HR policy documents through a conversational
Streamlit interface. The application uses Retrieval-Augmented Generation
(RAG) to retrieve relevant information from enterprise PDF documents and
generate context-grounded answers using Mistral through Ollama.

## ✨ Features

-   🔐 **User Authentication** --- Login-based access before users can
    query the HR assistant.
-   📄 **PDF Document Processing** --- Loads HR policy PDFs using
    LangChain's PDF loader.
-   ✂️ **Document Chunking** --- Splits documents into 500-character
    chunks with a 50-character overlap.
-   🧠 **Semantic Embeddings** --- Converts document chunks into vector
    representations using HuggingFace embeddings.
-   🗃️ **Vector Search** --- Stores document embeddings in Chroma and
    performs similarity search.
-   🔎 **Top-K Retrieval** --- Retrieves the top 3 most relevant
    document chunks for each user query.
-   🤖 **Context-Grounded Generation** --- Sends the retrieved context
    and user question to the Mistral LLM through Ollama.
-   💬 **Streamlit Interface** --- Provides a simple web interface for
    authentication and HR questions.
-   🏷️ **Source Metadata** --- Associates retrieved documents with their
    original PDF filename.

## 🏗️ Architecture

``` text
                    ┌──────────────────────┐
                    │      Streamlit UI    │
                    │  Login + User Query  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Authentication      │
                    │      auth.py         │
                    └──────────┬───────────┘
                               │
                         Authenticated
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PDF Documents      │
                    │   hr_policy.pdf      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Loading &   │
                    │ Chunking (500/50)    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ HuggingFace          │
                    │ Embeddings            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Chroma          │
                    │   Vector Store       │
                    └──────────┬───────────┘
                               │
                    Similarity Search k=3
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Retrieved Context    │
                    │ + User Question      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Mistral via Ollama   │
                    │   rag_pipeline.py   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Grounded HR Answer   │
                    └──────────────────────┘
```

## 🔄 RAG Pipeline

The project follows a straightforward Retrieval-Augmented Generation
workflow:

1.  **Load documents**\
    HR policy PDFs are loaded from the `documents/` directory using
    `PyPDFLoader`.

2.  **Attach metadata**\
    Each loaded document is tagged with its source PDF filename.

3.  **Split documents**\
    Documents are divided into chunks of **500 characters** with a
    **50-character overlap**.

4.  **Generate embeddings**\
    HuggingFace embeddings are generated for the document chunks.

5.  **Store vectors**\
    The embedded chunks are stored in a **Chroma vector database**.

6.  **Retrieve relevant context**\
    When the user submits a question, Chroma performs similarity search
    and returns the **top 3 relevant chunks**.

7.  **Generate an answer**\
    The retrieved chunks are combined into a context string and supplied
    to **Mistral via Ollama** together with the user's question.

8.  **Display the response**\
    The generated answer is displayed through the Streamlit interface.

## 📁 Project Structure

``` text
enterprise_auth_rag/
│
├── app.py
├── auth.py
├── vectorstore.py
├── rag_pipeline.py
├── memory.py
│
├── documents/
│   └── hr_policy.pdf
│
└── ...
```

### File Responsibilities

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `app.py`                            Streamlit UI, login flow, query
                                      handling, retrieval and response
                                      display

  `auth.py`                           Basic username/password
                                      authentication

  `vectorstore.py`                    PDF loading, metadata assignment,
                                      chunking, embeddings and Chroma
                                      vector store creation

  `rag_pipeline.py`                   Prompt construction and answer
                                      generation using Mistral through
                                      Ollama

  `memory.py`                         Defines a LangChain
                                      `ConversationBufferMemory` helper

  `documents/hr_policy.pdf`           Enterprise HR policy knowledge
                                      source
  -----------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python**
-   **Streamlit**
-   **LangChain**
-   **Chroma**
-   **HuggingFace Embeddings**
-   **Ollama**
-   **Mistral**
-   **PyPDFLoader**
-   **HR Policy PDF documents**

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd enterprise_auth_rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Set these environment variables before launching the application:

```text
HR_USERNAME=madhuri
HR_PASSWORD=<your-password>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<your-password>
```

### 5. Install and start Ollama

The application expects a local Ollama installation with the `mistral` model available.

```bash
ollama pull mistral
```

### 6. Run the application

```bash
streamlit run app.py
```

## 🚀 How It Works

After launching the application:

1.  The user enters a username and password.
2.  The authentication layer validates the credentials.
3.  After successful login, the HR query field becomes available.
4.  The application loads and processes the HR policy documents.
5.  The user's question is converted into a semantic search query.
6.  Chroma retrieves the three most relevant chunks.
7.  The retrieved context is passed to Mistral through Ollama.
8.  The model generates an answer based on the supplied context.
9.  The answer is displayed in the Streamlit application.

## ⚠️ Current Implementation Notes

This repository represents a working project implementation, but some
aspects are intentionally simple:

-   Authentication credentials are currently hard-coded in `auth.py`;
    this is suitable for a prototype but not production authentication.
-   The vector store is created when `load_vectorstore()` is called
    rather than being persisted as a separately managed production
    vector database.
-   The embedding model is created through LangChain's
    `HuggingFaceEmbeddings` default configuration; the repository does
    not explicitly specify an embedding model name.
-   `memory.py` defines conversation memory, but `app.py` does not
    currently use that memory in the query-generation flow. Therefore,
    persistent multi-turn conversational memory should **not** be
    claimed as an implemented feature.
-   The retrieved chunks are combined into a single context string
    before being passed to the LLM.
-   The current prompt instructs the model to answer based only on the
    supplied context.

## 🔮 Potential Improvements

For a production-oriented implementation, the following could be added:

-   Persist Chroma data instead of rebuilding the vector store for each
    query.
-   Use environment variables or a secure identity provider for
    authentication.
-   Explicitly configure and version the embedding model.
-   Integrate `ConversationBufferMemory` into the Streamlit query flow
    for true multi-turn conversations.
-   Add source citations to answers.
-   Add document upload support.
-   Add document-level access control for enterprise users.
-   Add evaluation metrics for retrieval quality and answer
    faithfulness.
-   Add caching for embeddings and vector-store initialization.
-   Containerize the application with Docker.
-   Add automated tests and logging.

## 📌 Resume Alignment

The project implementation supports the following resume claims:

-   **AI-powered HR assistant with user authentication** --- supported
    by `app.py` and `auth.py`.
-   **RAG pipeline with 500-character chunks and 50-character overlap**
    --- directly implemented in `vectorstore.py`.
-   **Top-3 retrieval from Chroma** --- directly implemented through
    similarity search with `k=3`.
-   **Embeddings + semantic retrieval** --- implemented using
    HuggingFace embeddings and Chroma similarity search.
-   **LangChain + Mistral via Ollama** --- implemented across
    `vectorstore.py` and `rag_pipeline.py`.
-   **PDF processing and enterprise-context-based responses** ---
    directly supported by the document loading and RAG flow.
