import os
import re
import uuid
from html import escape
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from lexiq import LexIQ


VECTOR_STORE_DIR = "chroma_db_legal_bot_part1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"


def clean_result(text: str) -> str:
    """Normalize extra blank lines in model output."""
    return re.sub(r"\n{3,}", "\n\n", text).strip()


class SimpleGroqLLM:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def __call__(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content


def load_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def load_vector_store(embeddings: HuggingFaceEmbeddings) -> Chroma:
    if not Path(VECTOR_STORE_DIR).exists():
        raise RuntimeError(
            "Vector database not found. Run `python ingest.py` once before starting the app."
        )

    return Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings,
    )


st.set_page_config(
    page_title="LexIQ - Legal Research Assistant",
    page_icon=":material/gavel:",
    layout="wide",
)

load_dotenv()

st.markdown(
    """
    <style>
    body { font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .block-container { max-width: 1120px; padding-top: 2rem; }
    .app-title { font-size: 3rem; font-weight: 750; margin-bottom: 0.25rem; }
    .app-subtitle { color: #4b5563; font-size: 1.05rem; margin-bottom: 1.5rem; }
    .status-line { color: #374151; font-size: 0.95rem; }
    .answer-box {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.25rem;
        background: #ffffff;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    .question-box {
        border-left: 4px solid #2563eb;
        padding: 0.75rem 1rem;
        background: #f8fafc;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">LexIQ</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Legal research assistant for Indian law, powered by local document retrieval and Groq.</div>',
    unsafe_allow_html=True,
)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Missing GROQ_API_KEY. Create a .env file using .env.example.")
    st.stop()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

with st.spinner("Loading retrieval pipeline..."):
    try:
        llm = SimpleGroqLLM(groq_api_key)
        embeddings = load_embeddings()
        vector_store = load_vector_store(embeddings)
        assistant = LexIQ(llm, embeddings, vector_store)
    except Exception as exc:
        st.error(f"Unable to load the application: {exc}")
        st.stop()

st.markdown(
    '<p class="status-line">Corpus loaded. Ask a question from the available Indian legal documents.</p>',
    unsafe_allow_html=True,
)

question = st.text_input(
    "Legal question",
    placeholder="Example: What is the punishment for theft under IPC?",
)

if question:
    with st.spinner("Searching the corpus and drafting an answer..."):
        try:
            result, _history = assistant.conversational(
                question, st.session_state.thread_id
            )
            safe_question = escape(question)
            safe_result = escape(clean_result(result))
            st.markdown(
                f'<div class="question-box"><strong>Question:</strong> {safe_question}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="answer-box">{safe_result}</div>', unsafe_allow_html=True
            )
        except Exception as exc:
            st.error(f"Unable to answer the question: {exc}")

st.caption(
    "LexIQ provides legal information for study and research. It does not provide legal advice."
)
