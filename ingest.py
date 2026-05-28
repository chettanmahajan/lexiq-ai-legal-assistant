import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_FILES = [
    Path("docs/Constitution_of_India.pdf"),
    Path("docs/CrPC.pdf"),
    Path("docs/IPC_1860.pdf"),
]
VECTOR_STORE_DIR = "chroma_db_legal_bot_part1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def load_documents(pdf_files):
    documents = []

    for pdf_file in pdf_files:
        if not pdf_file.exists():
            logger.warning("Skipping missing file: %s", pdf_file)
            continue

        logger.info("Loading %s", pdf_file)
        documents.extend(PyPDFLoader(str(pdf_file)).load())

    logger.info("Loaded %s pages", len(documents))
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    logger.info("Created %s chunks", len(chunks))
    return chunks


def store_embeddings(chunks, embeddings):
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings,
    )
    vector_store.add_documents(chunks)
    logger.info("Stored embeddings in %s", VECTOR_STORE_DIR)


def main():
    logger.info("Starting ingestion")

    embeddings = load_embeddings()
    documents = load_documents(PDF_FILES)

    if not documents:
        raise RuntimeError("No documents were loaded. Check the files in docs/.")

    chunks = chunk_documents(documents)
    store_embeddings(chunks, embeddings)

    logger.info("Ingestion completed")


if __name__ == "__main__":
    main()
