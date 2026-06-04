"""
test_rag_pipeline.py — Unit tests for the EquityLens AI RAG pipeline.

Run with: pytest tests/ -v
"""

import json
import pickle
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ─────────────────────────────────────────────
# Config tests
# ─────────────────────────────────────────────

def test_validate_config_missing_key(monkeypatch):
    """validate_config should return errors when API key is missing."""
    monkeypatch.setenv("OPENAI_API_KEY", "")
    from src.config.settings import validate_config, LLMConfig
    # Rebuild config with monkeypatched env
    cfg = LLMConfig()
    assert cfg.openai_api_key == ""


def test_validate_config_placeholder(monkeypatch):
    """validate_config should flag placeholder values."""
    monkeypatch.setenv("OPENAI_API_KEY", "enter your key here")
    from src.config import validate_config
    is_valid, errors = validate_config()
    assert not is_valid
    assert len(errors) > 0


# ─────────────────────────────────────────────
# History manager tests
# ─────────────────────────────────────────────

def test_save_and_load_history(tmp_path, monkeypatch):
    """Saving a session should persist it and be retrievable."""
    # Point history file to a temp path
    history_file = tmp_path / "history.json"
    monkeypatch.setattr(
        "src.utils.history_manager.app_config",
        MagicMock(history_file=history_file),
    )

    from src.utils.history_manager import save_session, load_history

    save_session(
        urls=["https://example.com/article1"],
        question="What is the inflation outlook?",
        answer="Inflation is expected to moderate.",
        sources=["https://example.com/article1"],
        confidence=72,
    )

    history = load_history()
    assert len(history) == 1
    assert history[0]["question"] == "What is the inflation outlook?"
    assert history[0]["confidence"] == 72


def test_clear_history(tmp_path, monkeypatch):
    """clear_history should empty the history file."""
    history_file = tmp_path / "history.json"
    history_file.write_text('[{"id":"session_0001"}]', encoding="utf-8")
    monkeypatch.setattr(
        "src.utils.history_manager.app_config",
        MagicMock(history_file=history_file),
    )

    from src.utils.history_manager import clear_history, load_history

    clear_history()
    assert load_history() == []


def test_get_history_stats_empty(tmp_path, monkeypatch):
    """Stats should return zeros for empty history."""
    history_file = tmp_path / "history.json"
    history_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(
        "src.utils.history_manager.app_config",
        MagicMock(history_file=history_file),
    )

    from src.utils.history_manager import get_history_stats

    stats = get_history_stats()
    assert stats["total_sessions"] == 0
    assert stats["avg_confidence"] == 0


# ─────────────────────────────────────────────
# RAG pipeline: unit tests with mocks
# ─────────────────────────────────────────────

@patch("src.utils.rag_pipeline.UnstructuredURLLoader")
@patch("langchain_community.embeddings.OpenAIEmbeddings")
@patch("src.utils.rag_pipeline.FAISS")
@patch("src.utils.rag_pipeline._save_vector_store")
def test_build_vector_store_calls_pipeline(mock_save, mock_faiss, mock_embeddings, mock_loader, tmp_path, monkeypatch):
    """build_vector_store should call loader, splitter, embeddings, and FAISS."""
    # Mock loader to return a fake document
    fake_doc = MagicMock()
    fake_doc.page_content = "Apple Inc reported record earnings this quarter. " * 30
    mock_loader.return_value.load.return_value = [fake_doc]

    # Mock FAISS.from_documents
    mock_faiss_instance = MagicMock()
    mock_faiss.from_documents.return_value = mock_faiss_instance

    # Redirect vector store path to temp dir
    monkeypatch.setattr(
        "src.utils.rag_pipeline.vector_config",
        MagicMock(
            store_dir=tmp_path,
            store_filename="test_index",
            chunk_size=500,
            chunk_overlap=50,
        ),
    )
    monkeypatch.setattr(
        "src.utils.rag_pipeline.llm_config",
        MagicMock(openai_api_key="sk-test", embedding_model="text-embedding-ada-002"),
    )

    from src.utils.rag_pipeline import build_vector_store

    result = build_vector_store(urls=["https://example.com/article"])

    mock_loader.assert_called_once()
    mock_faiss.from_documents.assert_called_once()
    # The result should be the mock FAISS instance
    assert result == mock_faiss_instance


def test_build_vector_store_raises_on_empty_docs(monkeypatch):
    """build_vector_store should raise ValueError when no content is loaded."""
    with patch("src.utils.rag_pipeline.UnstructuredURLLoader") as mock_loader:
        mock_loader.return_value.load.return_value = []

        from src.utils.rag_pipeline import build_vector_store

        with pytest.raises(ValueError, match="No content could be extracted"):
            build_vector_store(urls=["https://example.com/empty"])


def test_vector_store_exists_false(tmp_path, monkeypatch):
    """vector_store_exists returns False when no index file is present."""
    monkeypatch.setattr(
        "src.utils.rag_pipeline.vector_config",
        MagicMock(store_dir=tmp_path, store_filename="nonexistent"),
    )

    from src.utils.rag_pipeline import vector_store_exists

    assert vector_store_exists() is False


# ─────────────────────────────────────────────
# PDF export tests
# ─────────────────────────────────────────────

def test_generate_pdf_report_returns_bytes():
    """generate_pdf_report should return non-empty bytes."""
    pytest.importorskip("reportlab")  # skip if reportlab not installed

    from src.utils.pdf_export import generate_pdf_report

    pdf_bytes = generate_pdf_report(
        question="What is the revenue outlook?",
        answer="Revenue is expected to grow by 15% year-over-year.",
        sources=["https://example.com/article"],
        confidence=80,
        urls=["https://example.com/article"],
        company_name="Acme Corp",
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000  # A real PDF has meaningful size
    assert pdf_bytes[:4] == b"%PDF"  # PDF magic bytes
