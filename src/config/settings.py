"""
settings.py — Centralized application configuration.
Loads all settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


@dataclass
class LLMConfig:
    """LLM and embedding configuration."""
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model_name: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-3.5-turbo-instruct"))
    temperature: float = 0.7
    max_tokens: int = 800
    embedding_model: str = "text-embedding-ada-002"


@dataclass
class VectorStoreConfig:
    """FAISS vector store configuration."""
    store_dir: Path = field(default_factory=lambda: ROOT_DIR / "data" / "vector_store")
    store_filename: str = "faiss_index"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    k_retrieval: int = 4  # number of docs to retrieve


@dataclass
class AppConfig:
    """Streamlit application configuration."""
    title: str = "EquityLens AI"
    subtitle: str = "Institutional-Grade Equity Research Powered by AI"
    max_urls: int = 5
    history_file: Path = field(default_factory=lambda: ROOT_DIR / "data" / "history" / "research_history.json")
    version: str = "2.0.0"


# Singleton instances used throughout the app
llm_config = LLMConfig()
vector_config = VectorStoreConfig()
app_config = AppConfig()


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate that required configuration values are set.

    Returns:
        (is_valid, list_of_error_messages)
    """
    errors: list[str] = []

    if not llm_config.openai_api_key or llm_config.openai_api_key.startswith("enter"):
        errors.append("OPENAI_API_KEY is not set. Please add it to your .env file.")

    return len(errors) == 0, errors
