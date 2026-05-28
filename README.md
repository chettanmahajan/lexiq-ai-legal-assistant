# LexIQ

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)

LexIQ is a Streamlit-based legal research assistant for Indian law. It uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant passages from local legal PDFs and generate structured answers with Groq.

This project is intended for legal information and study support only. It is not a substitute for advice from a qualified advocate.

## Features

- Question answering over Indian legal documents
- Local document embeddings with `sentence-transformers`
- ChromaDB vector storage for retrieval
- Groq-powered response generation
- Streamlit interface for interactive use
- Simple ingestion workflow for adding more PDFs

## Tech Stack

- Python 3.11+
- Streamlit
- LangChain
- ChromaDB
- sentence-transformers
- Groq
- pypdf

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/chettanmahajan/lexiq-ai-legal-assistant.git
cd lexiq-ai-legal-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file from the example file:

```bash
copy .env.example .env
```

On macOS / Linux:

```bash
cp .env.example .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Build the vector database

The vector database is generated locally from the PDFs in `docs/`.

```bash
python ingest.py
```

This creates `chroma_db_legal_bot_part1/`, which is intentionally excluded from Git.

### 6. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Example Questions

```text
What is the punishment for theft under IPC?
What are the fundamental rights under the Constitution of India?
What is the procedure after an FIR is filed?
```

## Project Structure

```text
lexiq-ai-legal-assistant/
|-- app.py                     # Streamlit application
|-- lexiq.py                   # RAG and chat logic
|-- ingest.py                  # PDF ingestion and vector store setup
|-- prompts.py                 # Prompt templates
|-- docs/                      # Source legal PDFs
|-- .streamlit/config.toml     # Streamlit configuration
|-- .env.example               # Environment variable template
|-- requirements.txt           # Runtime dependencies
|-- pyproject.toml             # Project metadata
|-- .gitignore
`-- LICENSE
```

## Current Corpus

The repository includes the following source documents:

- Constitution of India
- Code of Criminal Procedure
- Indian Penal Code, 1860

Additional PDFs can be added to `docs/`. Update `PDF_FILES` in `ingest.py` and run the ingestion script again.

## Limitations

- The app only answers from the documents available in the local corpus.
- Scanned or image-only PDFs may not parse correctly.
- Generated answers should be verified against primary legal sources.
- LexIQ does not provide legal advice.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
