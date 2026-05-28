import logging
import threading

from prompts import QA_PROMPT, SYSTEM_PROMPT


logger = logging.getLogger(__name__)


class LexIQ:
    """Core retrieval and answer-generation workflow."""

    store = {}
    store_lock = threading.Lock()

    def __init__(self, llm, embeddings, vector_store):
        self.llm = llm
        self.embeddings = embeddings
        self.vector_store = vector_store

    def get_session_history(self, session_id):
        with LexIQ.store_lock:
            if session_id not in LexIQ.store:
                LexIQ.store[session_id] = []
        return LexIQ.store[session_id]

    def conversational(self, query, session_id):
        logger.info("Incoming query: %s", query)
        history = self.get_session_history(session_id)

        try:
            docs = self.vector_store.similarity_search(query, k=3)
            context = "\n\n".join(doc.page_content for doc in docs)
        except Exception:
            logger.exception("Vector retrieval failed")
            context = "No relevant legal context could be retrieved."

        final_prompt = f"""
{SYSTEM_PROMPT}

Relevant Legal Context:
{context or "No relevant legal context found."}

{QA_PROMPT}

Question:
{query}
"""

        try:
            answer = self.llm(final_prompt)
        except Exception as exc:
            logger.exception("Answer generation failed")
            answer = f"Unable to generate an answer: {exc}"

        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})

        return answer, history
