# LexIQ

A small legal research assistant for Indian law. Ask a question in plain English, and LexIQ retrieves relevant passages from the included bare acts, then returns a structured answer.

LexIQ runs locally with Streamlit. Retrieval is handled with ChromaDB and sentence-transformers, while answer generation uses a Groq-hosted Llama model.

> Note: this project is for study and quick reference only. It is not legal advice. Always verify important information against the primary source or consult a qualified advocate.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

## Features

- Ask legal questions in plain English
- Retrieve answers from local Indian legal PDFs
- Build a local vector database with ChromaDB
- Use local embeddings through `sentence-transformers`
- Generate structured answers with Groq
- Add more PDF documents by updating the ingestion list

## How It Works

1. `ingest.py` reads the PDFs in `docs/`.
2. The text is split into chunks and embedded with `all-MiniLM-L6-v2`.
3. Chunks are stored in a local ChromaDB vector database.
4. `app.py` retrieves the most relevant chunks for each question.
5. Groq generates the final answer from the retrieved context.

## Requirements

- Python 3.11 or newer
- A Groq API key from https://console.groq.com/keys

## Setup

Clone the repository:

```bash
git clone https://github.com/chettanmahajan/lexiq-ai-legal-assistant.git
cd lexiq-ai-legal-assistant
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
copy .env.example .env
```

For macOS or Linux:

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Build the vector database:

```bash
python ingest.py
```

Run the app:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Example Questions

```text
What is the punishment for theft under IPC?
What are the fundamental rights under the Constitution of India?
What happens after an FIR is filed?
```

## Project Structure

```text
.
|-- app.py                 # Streamlit application
|-- lexiq.py               # Retrieval and answer generation logic
|-- ingest.py              # PDF ingestion and vector database builder
|-- prompts.py             # Prompt templates
|-- docs/                  # Source legal PDFs
|-- .streamlit/            # Streamlit configuration
|-- .env.example           # Environment variable template
|-- .gitignore             # Keeps secrets and generated files out of Git
|-- requirements.txt       # Python dependencies
|-- pyproject.toml         # Project metadata
`-- LICENSE
```

## Included Legal Documents

- Constitution of India
- Indian Penal Code, 1860
- Code of Criminal Procedure

## Adding Documents

Add a PDF to `docs/`, update the `PDF_FILES` list in `ingest.py`, and run:

```bash
python ingest.py
```

The app works best with text-based PDFs. Scanned or image-only PDFs may require OCR before ingestion.

## Files That Should Not Be Committed

The real `.env` file, virtual environments, logs, caches, and the generated ChromaDB folder are intentionally excluded by `.gitignore`.

The `.env.example` file is safe to commit because it contains only placeholder values.

## License

Apache 2.0. See [LICENSE](LICENSE) for details.
