"""
history_manager.py — Persist and retrieve research session history.

Each session records:
  - timestamp
  - URLs processed
  - questions asked + answers + sources
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.config import app_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _ensure_history_file() -> Path:
    """Create the history file and parent directories if they don't exist."""
    path: Path = app_config.history_file
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    return path


def load_history() -> list[dict]:
    """
    Load all past research sessions from disk.

    Returns:
        List of session dicts, newest first.
    """
    path = _ensure_history_file()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(reversed(data))  # newest first
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to load history: %s", exc)
        return []


def save_session(
    urls: list[str],
    question: str,
    answer: str,
    sources: list[str],
    confidence: int,
) -> None:
    """
    Append a new Q&A record to the research history.

    Args:
        urls: URLs that were processed in this session.
        question: User's question.
        answer: LLM-generated answer.
        sources: Source URLs cited by the answer.
        confidence: Computed confidence score (0–100).
    """
    path = _ensure_history_file()
    try:
        history: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        history = []

    record = {
        "id": f"session_{len(history) + 1:04d}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "urls": urls,
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }
    history.append(record)

    try:
        path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Saved session to history (total=%d)", len(history))
    except OSError as exc:
        logger.error("Failed to save history: %s", exc)


def clear_history() -> None:
    """Delete all stored research history."""
    path = _ensure_history_file()
    path.write_text("[]", encoding="utf-8")
    logger.info("Research history cleared.")


def get_history_stats() -> dict:
    """Return aggregate stats about the research history."""
    history = load_history()
    return {
        "total_sessions": len(history),
        "total_urls": sum(len(s.get("urls", [])) for s in history),
        "avg_confidence": (
            int(sum(s.get("confidence", 0) for s in history) / len(history))
            if history else 0
        ),
    }
