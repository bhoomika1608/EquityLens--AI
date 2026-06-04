"""
rag_pipeline.py — Core RAG (Retrieval-Augmented Generation) pipeline.

Handles:
  - URL content loading
  - Text splitting / chunking
  - OpenAI embedding generation
  - FAISS vector store creation & persistence
  - Retrieval QA chain execution
"""

import time
import pickle
from pathlib import Path
from typing import Callable, Optional

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain

from src.config import llm_config, vector_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────────
# Vector Store Management
# ─────────────────────────────────────────────

def _get_store_path() -> Path:
    """Return the full path to the persisted FAISS pickle file."""
    path = vector_config.store_dir / f"{vector_config.store_filename}.pkl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def vector_store_exists() -> bool:
    """Check whether a persisted vector store exists on disk."""
    return _get_store_path().exists()


def load_vector_store() -> Optional[FAISS]:
    """
    Load the persisted FAISS vector store from disk.

    Returns:
        FAISS instance, or None if not found.
    """
    store_path = _get_store_path()
    if not store_path.exists():
        logger.warning("No vector store found at %s", store_path)
        return None

    logger.info("Loading vector store from %s", store_path)
    with open(store_path, "rb") as f:
        return pickle.load(f)


def _save_vector_store(store: FAISS) -> None:
    """Persist the FAISS vector store to disk using pickle."""
    store_path = _get_store_path()
    logger.info("Saving vector store to %s", store_path)
    with open(store_path, "wb") as f:
        pickle.dump(store, f)


# ─────────────────────────────────────────────
# Pipeline: Build Index from URLs
# ─────────────────────────────────────────────

def build_vector_store(
    urls: list[str],
    progress_callback: Optional[Callable[[str, int], None]] = None,
) -> FAISS:
    """
    Full RAG ingestion pipeline: load → split → embed → index.

    Args:
        urls: List of news article URLs to process.
        progress_callback: Optional fn(message, percent) for UI progress updates.

    Returns:
        Built FAISS vector store.

    Raises:
        ValueError: If no content could be loaded from the URLs.
        RuntimeError: If embedding or indexing fails.
    """

    def _progress(msg: str, pct: int) -> None:
        logger.info("[%d%%] %s", pct, msg)
        if progress_callback:
            progress_callback(msg, pct)

    # ── Step 1: Load documents from URLs ──
    _progress("Loading articles from URLs…", 10)
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()

    if not documents:
        raise ValueError(
            "No content could be extracted from the provided URLs. "
            "Please check that the URLs are accessible and contain readable text."
        )
    logger.info("Loaded %d document(s) from %d URL(s)", len(documents), len(urls))

    # ── Step 2: Split into chunks ──
    _progress("Splitting text into chunks…", 35)
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", ", "],
        chunk_size=vector_config.chunk_size,
        chunk_overlap=vector_config.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    logger.info("Split into %d chunks (size=%d, overlap=%d)",
                len(chunks), vector_config.chunk_size, vector_config.chunk_overlap)

    # ── Step 3: Generate embeddings ──
    _progress("Generating semantic embeddings…", 60)
    embeddings = OpenAIEmbeddings(
        openai_api_key=llm_config.openai_api_key,
        model=llm_config.embedding_model,
    )

    # ── Step 4: Build FAISS index ──
    _progress("Building FAISS vector index…", 80)
    vector_store = FAISS.from_documents(chunks, embeddings=embeddings)

    # ── Step 5: Persist to disk ──
    _progress("Saving index to disk…", 95)
    _save_vector_store(vector_store)

    _progress("Index built successfully!", 100)
    time.sleep(0.5)  # brief pause so progress UI registers 100%
    return vector_store


# ─────────────────────────────────────────────
# Pipeline: Query the Index
# ─────────────────────────────────────────────

def query_vector_store(question: str) -> dict:
    """
    Run a RAG query against the persisted vector store.

    Args:
        question: The user's natural-language question.

    Returns:
        dict with keys: "answer" (str), "sources" (list[str]), "confidence" (float)

    Raises:
        FileNotFoundError: If no vector store has been built yet.
        RuntimeError: If the LLM chain fails.
    """
    vector_store = load_vector_store()
    if vector_store is None:
        raise FileNotFoundError(
            "No research data found. Please process some article URLs first."
        )

    logger.info("Running RAG query: %r", question[:80])

    # Instantiate the LLM
    llm = OpenAI(
        openai_api_key=llm_config.openai_api_key,
        model_name=llm_config.model_name,
        temperature=llm_config.temperature,
        max_tokens=llm_config.max_tokens,
    )

    # Build retrieval chain
    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(
            search_kwargs={"k": vector_config.k_retrieval}
        ),
    )

    # Execute query
    raw_result: dict = chain({"question": question}, return_only_outputs=True)

    # Parse and normalise sources
    raw_sources: str = raw_result.get("sources", "")
    sources_list: list[str] = (
        [s.strip() for s in raw_sources.split("\n") if s.strip()]
        if raw_sources
        else []
    )

    # Compute a simple heuristic confidence score (0–100)
    answer_len = len(raw_result.get("answer", ""))
    confidence = min(100, max(40, int(answer_len / 8)))

    result = {
        "answer": raw_result.get("answer", "No answer generated."),
        "sources": sources_list,
        "confidence": confidence,
    }

    logger.info("Query completed. Answer length=%d, Sources=%d, Confidence=%d%%",
                answer_len, len(sources_list), confidence)
    return result
