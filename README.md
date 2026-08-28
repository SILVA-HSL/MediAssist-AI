
# MediAssist AI

MediAssist AI is a local hospital information assistant that uses Retrieval-Augmented Generation (RAG). It searches hospital documents stored in ChromaDB and uses an Ollama language model to answer questions based only on the retrieved information.

## Features

- Stores hospital documents in a persistent ChromaDB collection
- Generates embeddings using `all-MiniLM-L6-v2`
- Retrieves relevant document chunks for a question
- Uses Ollama with the `llama3.2` model
- Provides answers grounded in the hospital documents
- Includes a fallback response when information is not found

## Project Structure

```text
MediAssist AI/
├── chroma_db/
├── documents/
│   ├── emergency_procedure.txt
│   ├── medication_policy.txt
│   └── patient_admission.txt
├── src/
│   ├── `chat.py`
│   ├── `chroma_db_client.py`
│   └── `search.py`
├── `requirements.txt`
└── `README.md`
```

## Requirements

- Python 3.9 or later
- Ollama
- The Ollama `llama3.2` model

## Installation

Clone or download the project, then install the Python dependencies:

```bash
pip install -r `requirements.txt`
```

Install Ollama from:

https://ollama.com/

After installing Ollama, download the language model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before using the chat application.

## Usage

The scripts use relative paths, so run them from the `src` directory.

### 1. Index the hospital documents

```bash
cd src
python `chroma_db_client.py`
```

This reads the text files from `documents/`, creates embeddings, and stores the document chunks in ChromaDB.

### 2. Test document retrieval

```bash
python `search.py`
```

This retrieves and displays the most relevant document chunks for a sample question.

### 3. Ask questions using the AI assistant

```bash
python `chat.py`
```

Enter a hospital-related question when prompted. The assistant will retrieve relevant information and generate an answer using the Ollama model.

## Example Questions

- What should healthcare staff do if a patient has a drug allergy?
- What should be checked before giving medication?
- How should critical patients be handled?

## How It Works

1. Hospital text documents are loaded from the `documents/` directory.
2. Documents are divided into smaller chunks.
3. Each chunk is converted into an embedding using `all-MiniLM-L6-v2`.
4. Embeddings and document metadata are stored in ChromaDB.
5. A user's question is converted into an embedding.
6. ChromaDB retrieves the most relevant document chunks.
7. The retrieved content is provided as context to the Ollama language model.
8. The assistant generates an answer using only the supplied context.

## Resources

This project was developed using the following resources:

- [Chroma Getting Started Documentation](https://docs.trychroma.com/docs/overview/getting-started)
- [LangChain](https://www.langchain.com/langchain)
- [Ollama](https://ollama.com/)

## Disclaimer

MediAssist AI is an educational project and should not replace professional medical advice, clinical judgment, or official hospital procedures. Always verify information with qualified healthcare professionals and approved clinical documentation.
